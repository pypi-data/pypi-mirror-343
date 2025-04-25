import sys
from .dataframe_toolkit import generate_epoch


def get_streamlit_token():
    if 'streamlit' in sys.modules:
        st = sys.modules['streamlit']
        if st.query_params is not None and "auth_token" in st.query_params:
            auth_token = st.query_params["auth_token"]
            return auth_token


def get_streamlit_domain():
    if 'streamlit' in sys.modules:
        st = sys.modules['streamlit']
        if st.query_params is not None and "dsapi" in st.query_params:
            domain = st.query_params["dsapi"]
            return domain


def get_streamlit_from() -> int:
    """
    timestamp representation of from parameter on UI (ms)
    :return:
    """
    if 'streamlit' in sys.modules:
        st = sys.modules['streamlit']
        if st.query_params is not None and "from" in st.query_params:
            param = st.query_params["from"]
            if 'now' in param:
                return generate_epoch(param)
            else:
                return int(param)


def get_streamlit_to() -> int:
    """
    timestamp representation of to parameter on UI (ms)
    :return:
    """
    if 'streamlit' in sys.modules:
        st = sys.modules['streamlit']
        if st.query_params is not None and "to" in st.query_params:
            param = st.query_params["to"]
            if 'now' in param:
                return generate_epoch(param)
            else:
                return int(param)
