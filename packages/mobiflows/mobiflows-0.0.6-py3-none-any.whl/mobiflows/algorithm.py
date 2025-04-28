from collections import defaultdict
from datetime import timedelta

import geopandas as gpd
import pandas as pd
import polars as pl


class CellTrajectory:
    def __init__(
        self,
        tdf: pl.DataFrame,
        v_id_col: str = "v_id",
        time_col: str = "datetime",
        uid_col: str = "uid",
    ) -> None:
        """
        Parameters
        ----------
        tdf : pandas.DataFrame
            Trajectory data with columns [uid, datetime, longitude, latitude]
            with regular observations for every users (interval τ,
            a balanced panel)
        v_id_col : str, optional
            The name of the column in the data containing the cell ID
            (default is "v_id")
        time_col : str, optional
            Time column name (default "time")
        uid_col : str, optional
            User ID column name (default "uid")
        """

        super().__init__()
        self.tdf = tdf.sort(by=[uid_col, time_col])
        self.v_id = v_id_col
        self.time = time_col
        self.uid = uid_col

        if self.v_id not in tdf.columns:
            raise TypeError(
                """Cell trajectory dataframe does not contain 
                cell IDs or cell IDs column does not match what was set."""
            )
        if self.time not in tdf.columns:
            raise TypeError(
                """Cell trajectory dataframe does not contain a time
                column or time column does not match what was set."""
            )
        if self.uid not in tdf.columns:
            raise TypeError(
                """Cell trajectory dataframe does not contain a uid
                column or uid column does not match what was set."""
            )

    def get_tdf(self) -> pl.DataFrame:
        """getter"""
        return self.tdf

    def build_voronoi_flows(self, tau: int = 30, w: int = 60) -> pl.DataFrame:
        """build voronoi flows

        Parameters
        ----------
        tau : int
            time resolution of data in minutes
        w : int
            Duration at a location used to define a trip in minutes

        Returns
        -------
        polars.DataFrame
            Polars dataframe with the columns
                [origin, dest, time]
        """

        d = w // tau + 1
        tdf = self.tdf.sort(["uid", "datetime"])

        # create a dictionary: uid -> list of (datetime, v_id)
        user_locations = defaultdict(list)
        for row in tdf.iter_rows(named=True):
            user_locations[row["uid"]].append((row["datetime"], row["v_id"]))

        voronoi_cells = tdf["v_id"].unique().to_list()

        # precompute stayers: {(cell, time): set of users}
        stayers = defaultdict(set)

        for user, locs in user_locations.items():
            times = [t for t, _ in locs]
            cells = [v for _, v in locs]

            for h in range(d - 1, len(times)):
                if all(cells[h - i] == cells[h] for i in range(d)):
                    stayers[(cells[h], times[h])].add(user)

        # precompute movers: {(cell, time): set of users}
        movers = defaultdict(set)
        for v, t in stayers:
            if (v, t + timedelta(minutes=tau)) in stayers:
                movers[(v, t)] = (
                    stayers[(v, t)] - stayers[(v, t + timedelta(minutes=tau))]
                )
            else:
                movers[(v, t)] = stayers[(v, t)]

        # compute trips
        trips_list = []

        for (v_q, t_h), users in movers.items():
            for u in users:
                h_prime = t_h + timedelta(minutes=tau)
                while True:
                    found = False
                    for v_q_prime in voronoi_cells:
                        if (v_q_prime, h_prime) in stayers and u in stayers[
                            (v_q_prime, h_prime)
                        ]:
                            trips_list.append((v_q, v_q_prime, t_h))
                            found = True
                            break
                    if found or h_prime > max(t for _, t in stayers.keys()):
                        break
                    h_prime += timedelta(minutes=tau)

        trips_df = pl.DataFrame(
            trips_list, schema=["origin", "dest", "time"], orient="row"
        )
        v_flows = trips_df.group_by(["origin", "dest", "time"]).agg(count=pl.len())

        return v_flows

    def build_zipcode_flows(
        self,
        cell_flows: pl.DataFrame,
        voronoi_zipcode_intersection_proportions: pl.DataFrame,
    ) -> pl.DataFrame:
        """build zipcode flows"""

        flows = (
            (
                cell_flows.join(
                    voronoi_zipcode_intersection_proportions,
                    left_on="origin",
                    right_on="v_id",
                    suffix="_origin",
                    how="left",
                )
                .join(
                    voronoi_zipcode_intersection_proportions,
                    left_on="dest",
                    right_on="v_id",
                    suffix="_dest",
                    how="left",
                )
                .rename({"p": "p_origin", "plz": "plz_origin"})
                .with_columns(p=pl.col("p_origin") * pl.col("p_dest"))
                .with_columns(count_avg=pl.col("p") * pl.col("count"))
                .select(
                    origin=pl.col("plz_origin"),
                    dest=pl.col("plz_dest"),
                    time=pl.col("time"),
                    p=pl.col("p"),
                    count_avg=pl.col("count_avg"),
                )
            )
            .group_by(["origin", "dest", "time"])
            .agg(count_avg=pl.sum("count_avg"))
            .with_columns(count=pl.col("count_avg").floor().cast(pl.Int64))
            .select(["origin", "dest", "time", "count"])
        )

        return flows


class Trajectory:
    def __init__(
        self,
        tdf: pl.DataFrame,
        longitude: str = "lon",
        latitude: str = "lat",
        v_id_col: str = "v_id",
        time_col: str = "datetime",
        uid_col: str = "uid",
    ) -> None:
        """
        Parameters
        ----------
        tdf : pandas.DataFrame
            Trajectory data with columns [uid, datetime, longitude, latitude]
            with regular observations for every users (interval τ,
            a balanced panel)
        longitude : str, optional
            The name of the column in the data containing the longitude
            (default is "lon")
        latitude : str, optional
            The name of the column in the data containing the latitude
            (default is "lat")
        v_id_col : str, optional
            Column identifying tile IDs in the tessellation dataframe
            (default is "v_id")
        time_col : str, optional
            Time column name (default "time")
        uid_col : str, optional
            User ID column name (default "uid")
        """

        super().__init__()
        self.tdf = tdf.sort(by=[uid_col, time_col])
        self.lon = longitude
        self.lat = latitude
        self.v_id = v_id_col
        self.time = time_col
        self.uid = uid_col

        if self.lon not in tdf.columns:
            raise TypeError(
                """Cell trajectory dataframe does not contain a longitude
                column or the longitude column does not match what was set."""
            )
        if self.lat not in tdf.columns:
            raise TypeError(
                """Cell trajectory dataframe does not contain a latitude
                column or the latitude column does not match what was set."""
            )

        if self.time not in tdf.columns:
            raise TypeError(
                """Cell trajectory dataframe does not contain a time
                column or time column does not match what was set."""
            )
        if self.uid not in tdf.columns:
            raise TypeError(
                """Cell trajectory dataframe does not contain a uid
                column or uid column does not match what was set."""
            )

    def mapping(self, tessellation: gpd.GeoDataFrame) -> CellTrajectory:
        """Map (pseudo-)locations to coverage cells

        Parameters
        ----------
        tessellation : geopandas.GeoDataFrame
            Tessellation, e.g., Voronoi tessellation and any coverage
            tessellation with columns [v_id, longitude, latitude, geometry]

        Returns
        -------
        polars.DataFrame
            Polars dataframe with the columns
            [uid, datetime, longitude, latitude, v_id]
        """

        if self.v_id not in tessellation.columns:
            raise TypeError(
                """Cell trajectory dataframe does not contain 
                cell IDs or cell IDs column does not match what was set."""
            )

        gdf = gpd.GeoDataFrame(
            self.tdf.to_pandas(),
            geometry=gpd.points_from_xy(self.tdf[self.lon], self.tdf[self.lat]),
            crs=tessellation.crs,
        )
        joined = gpd.sjoin(
            gdf, tessellation[[self.v_id, "geometry"]], how="left", predicate="within"
        )
        gdf[self.v_id] = joined[self.v_id]

        matched = gdf[~gdf[self.v_id].isna()]
        unmatched = gdf[gdf[self.v_id].isna()].copy()

        if not unmatched.empty:
            # build a lookup of future assigned regions per user
            tessellation = tessellation.copy()
            tessellation["rep"] = gpd.points_from_xy(
                tessellation[self.lon], tessellation[self.lat]
            )

            matched_sorted = matched.sort_values(by=[self.uid, self.time])
            future_region_lookup = matched_sorted.groupby(self.uid).apply(
                lambda df: df.set_index(self.time)[self.v_id], include_groups=False
            )

            # find candidate cells for all unmatched points (intersection test)
            unmatched["candidates"] = unmatched.geometry.apply(
                lambda geom: tessellation[tessellation.geometry.intersects(geom)][
                    [self.v_id, "rep"]
                ]
            )

            fallback_ids = []
            for _, row in unmatched.iterrows():
                uid = row[self.uid]
                time = row[self.time]

                # candidate cells at current time
                candidates = row["candidates"]
                if candidates.empty:
                    raise ValueError(
                        f"""tdf not proper: trajectory point for user {uid} at time
                            {time} intersects no tessellation cell."""
                    )

                # find user's next assigned cell
                if uid not in future_region_lookup:
                    raise ValueError(
                        f"""tdf not proper: uid {uid} does not have any point
                            assigned to a cell to a cell."""
                    )

                user_future = future_region_lookup[uid]
                future_times = user_future[user_future.index > time]

                if future_times.empty:
                    raise ValueError(
                        f"""tdf not proper: no future point for uid {uid} at time
                            {time}."""
                    )

                future_id = future_times.iloc[0]
                future_geom = tessellation.loc[
                    tessellation[self.v_id] == future_id, "rep"
                ].values[0]

                # choose closest candidate cell to the future one
                candidates["dist"] = candidates["rep"].distance(future_geom)
                fallback_id = candidates.sort_values(by="dist").iloc[0][self.v_id]
                fallback_ids.append(fallback_id)

            unmatched[self.v_id] = fallback_ids

            gdf = pd.concat(
                [matched, unmatched.drop(columns=["candidates"])], ignore_index=True
            )

        gdf.drop(columns=[self.lon, self.lat, "geometry"], inplace=True)

        return CellTrajectory(pl.DataFrame(gdf.sort_values(by=[self.uid, self.time])))
