import streamlit as st
from backend import load_data,load_data_plot, get_summary, plot_tracks
from pygwalker.api.streamlit import StreamlitRenderer

st.set_page_config(layout="wide")

tab1, tab2, tab3 = st.tabs(["dataframes","graphs","tableau"])

with tab1:
    
    data=load_data()
    data_plot=load_data_plot()
    summary=get_summary(data)

    st.write("### Most popular artists with the most popular song in their geners")
    st.dataframe(summary[0], hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        st.write("### Most popular artists by geners")
        st.dataframe(summary[2], width=900, hide_index=True)
    with col2:
        st.image("w24b_7fwr_210519.jpg")
        st.markdown('''https://www.freepik.com/free-vector/musical-melody-symbols-bright-blue-splotch_16463405.htm#query=music%20note%20png&position=3&from_view=keyword&track=ais&uuid=4e19278d-1e8f-4ae8-a892-2f3b37e41cf6">Image by brgfx</a> on Freepik")''')

    st.write("### Most popular songs by geners")
    st.dataframe(summary[1], hide_index=True)

with tab2:

    with st.sidebar:
        st.sidebar.header("For graphs content: Controls Raw Data and Graphs")
        years_data=st.sidebar.slider("Year", min_value=1960, max_value=2023, value=2023, step=1)

    filter_data_plot=data_plot[data_plot["album_year_release"]<=years_data]


    st.write("### Raw Data")
    st.dataframe(filter_data_plot, hide_index=True)

    st.write("### Graphs")
    plt=plot_tracks(filter_data_plot)
    st.pyplot(plt)
    
with tab3:
    st.write("pending")
    
    @st.cache_resource
    def get_pyg_renderer() -> "StreamlitRenderer":
        df = data
        # If you want to use feature of saving chart config, set `spec_io_mode="rw"`
        return StreamlitRenderer(df)


    renderer = get_pyg_renderer()

    renderer.explorer()
