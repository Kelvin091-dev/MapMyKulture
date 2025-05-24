# frontend/responsible_tourism_guide.py
import streamlit as st

def display_responsible_tourism_guide():
    st.header("🌿 Responsible Tourism Guide 🌍")
    st.write("Welcome to our guide on how to travel responsibly in India!")

    st.subheader("1. Respect Local Culture & Traditions")
    st.markdown("""
    * **Dress Appropriately:** Especially when visiting religious sites.
    * **Ask for Permission:** Before taking photos of people.
    * **Learn Basic Phrases:** A few words in the local language can go a long way.
    * **Support Local Artisans:** Buy directly from craftspeople to ensure fair wages.
    """)

    st.subheader("2. Support Local Economies")
    st.markdown("""
    * **Choose Local Businesses:** Stay in locally-owned guesthouses, eat at local restaurants.
    * **Hire Local Guides:** They provide authentic insights and direct income to the community.
    * **Buy Local Products:** Look for locally sourced goods and handicrafts.
    """)

    st.subheader("3. Minimize Environmental Impact")
    st.markdown("""
    * **Reduce, Reuse, Recycle:** Carry a reusable water bottle and avoid single-use plastics.
    * **Dispose of Waste Properly:** Don't litter, especially in natural areas.
    * **Conserve Resources:** Be mindful of water and energy usage.
    * **Stick to Marked Trails:** When hiking or exploring natural areas.
    """)

    st.subheader("4. Be Mindful of Wildlife")
    st.markdown("""
    * **Observe from a Distance:** Do not disturb animals in their natural habitat.
    * **Avoid Animal Exploitation:** Say no to elephant rides, snake charmers, or other activities that might harm animals.
    """)

    st.info("Your journey can make a positive impact! Travel thoughtfully.")