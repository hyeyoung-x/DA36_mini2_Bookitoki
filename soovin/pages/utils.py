# utils.py
import streamlit as st

def add_logo():
    st.markdown("""
    <style>
        .logo-text {
            font-weight:700 !important;
            font-size:30px !important;
            color: #ffffff !important;
            padding-left: 75px !important;
        }
        .logo-img {
            position: absolute;
            left: 25px;
            width: 50px !important;
            height: 50px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    title = st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="your_logo_url_here" alt="logo" class="logo-img">
            <p class="logo-text">Bookitoki</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    return title

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    st.markdown(nav_script, unsafe_allow_html=True)