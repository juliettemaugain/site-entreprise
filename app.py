import streamlit as st

st.title("Bienvenue sur mon Espace Pro")
st.write("La mise à jour a fonctionné ! Voici mes outils :")

# Un petit test interactif
if st.button("Lancer le test"):
    st.balloons()  # Ça va lancer des ballons sur l'écran !
    st.success("Bravo, ton site est interactif !")
    