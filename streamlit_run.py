def main():
    import numpy as np
    import pandas as pd
    import streamlit as st
    import supabase as supabase
    from supabase import create_client, Client
    import os
    import plotly.express as px

    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    print(supabase_key)
    print(supabase_url)
    if supabase_url and supabase_key:
        try:
            supabase: Client = create_client(supabase_url, supabase_key)

            df_to_supabase = pd.read_csv("marathon_results.csv")
            data_to_insert = df_to_supabase.to_dict(orient="records")
            table_check = supabase.table("marathon_times_full").select("rank").limit(1).execute()
            if not table_check.data:
                response = supabase.table("marathon_times_full").insert(data_to_insert).execute()

            df_to_supabase = pd.read_csv("half_marathon_results.csv")
            data_to_insert = df_to_supabase.to_dict(orient="records")
            table_check = supabase.table("half_marathon_times_full").select("rank").limit(1).execute()
            if not table_check.data:
                response = supabase.table("half_marathon_times_full").insert(data_to_insert).execute()

            df_to_supabase = pd.read_csv("results_10k.csv")
            data_to_insert = df_to_supabase.to_dict(orient="records")
            table_check = supabase.table("10k_times_full").select("rank").limit(1).execute()
            if not table_check.data:
                response = supabase.table("10k_times_full").insert(data_to_insert).execute()

            df_to_supabase = pd.read_csv("results_5k.csv")
            data_to_insert = df_to_supabase.to_dict(orient="records")
            table_check = supabase.table("5k_times_full").select("rank").limit(1).execute()
            if not table_check.data:
                response = supabase.table("5k_times_full").insert(data_to_insert).execute()

        except Exception as e:
            st.error(f"Error connecting to Supabase: {e}")

    @st.cache_data
    def load_data(limit, distance):
        if limit <= 1000:
            response = supabase.table(distance) \
                .select("*") \
                .range(0, limit - 1) \
                .execute()
            data = response.data
            return pd.DataFrame(data)

        all_data = []
        chunk_size = 1000
        start = 0
        while start < limit:
            end = min(start + chunk_size - 1, limit - 1)
            response = supabase.table(distance) \
                .select("*") \
                .range(start, end) \
                .execute()
            batch = response.data
            if not batch:
                break
            all_data.extend(batch)
            start += chunk_size

        return pd.DataFrame(all_data)
    
    def load_all_data(distance):
        all_data = []
        chunk_size = 1000
        start = 0

        while True:
            response = supabase.table(distance) \
                .select("*") \
                .range(start, start + chunk_size - 1) \
                .execute()
            batch = response.data
            if not batch:
                break
            all_data.extend(batch)
            if len(batch) < chunk_size:
                break
            start += chunk_size

        return pd.DataFrame(all_data)
    
    def get_slider(distance):
        if distance == "Marathon":
            return st.slider("Number of entries to include", 50, 5500, 2750, step=10)
        elif distance == "Half Marathon":
            return st.slider("Number of entries to include", 50, 10700, 5350, step=10)
        elif distance == "10k":
            return st.slider("Number of entries to include", 50, 7100, 3550, step=10)
        elif distance == "5k":
            return st.slider("Number of entries to include", 50, 6300, 3150, step=10)
        
    def get_table(distance):
        if distance == "Marathon":
            return "marathon_times_full"
        elif distance == "Half Marathon":
            return "half_marathon_times_full"
        elif distance == "10k":
            return "10k_times_full"
        elif distance == "5k":
            return "5k_times_full"

    selected_distance = st.selectbox("Choose a Race Distance:", ["Marathon", "Half Marathon", "10k", "5k"])

    st.title(selected_distance + " Data")

    # Bar Chart
    limit = get_slider(selected_distance)
    slider_df = load_data(limit, get_table(selected_distance))
    if "year" in slider_df.columns:
        year_counts = slider_df["year"].value_counts().sort_index()
        st.markdown("### Frequency of Top Times per Year in the " + selected_distance)
        st.bar_chart(year_counts)
    else:
        st.error("No 'year' column found in dataset")

    # Pie Chart
    if "country" in slider_df.columns:
        country_counts = slider_df["country"].value_counts()

        top_10 = country_counts.nlargest(10)
        others = country_counts.iloc[10:].sum()
        if others > 0:
            top_10["Other"] = others

        fig = px.pie(
            values=top_10.values,
            names=top_10.index,
            title="Top 10 Countries Breakdown",
            hole=0.3
        )

        st.plotly_chart(fig, use_container_width=True)

    df_all = load_all_data(get_table(selected_distance))
    if "year" in df_all.columns:
        cumulative_total = df_all.index + 1
        if selected_distance == "Half Marathon" or selected_distance == "Marathon":
            cumulative = (df_all["year"] >= 2017).cumsum()
            df_all["percent_since_2017"] = cumulative / cumulative_total * 100
        elif selected_distance == "10k" or selected_distance == "5k":
            cumulative = (df_all["year"] >= 2020).cumsum()
            df_all["percent_since_2020"] = cumulative / cumulative_total * 100

        df_plot = df_all.iloc[49:].copy()
        df_plot["cumulative_total"] = cumulative_total[49:]
        if selected_distance == "Half Marathon" or selected_distance == "Marathon":
            fig_line = px.line(
                df_plot,
                x="cumulative_total",
                y="percent_since_2017",
                title="Percentage of Top Times Since 2017 (Vaporfly 4% Hits the Market)"
            )
            fig_line.update_yaxes(title_text="Percentage (%)", range=[0, 100])
            fig_line.update_xaxes(title_text="Number of Entries Included")
            st.plotly_chart(fig_line, use_container_width=True)

        elif selected_distance == "10k" or selected_distance == "5k":
            fig_line = px.line(
                df_plot,
                x="cumulative_total",
                y="percent_since_2020",
                title="Percentage of Top Times Since 2020 (Dragonfly Hits the Market)"
            )
            fig_line.update_yaxes(title_text="Percentage (%)", range=[0, 100])
            fig_line.update_xaxes(title_text="Number of Entries Included")
            st.plotly_chart(fig_line, use_container_width=True)

if __name__ == "__main__":
    main()