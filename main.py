import streamlit as st

# Set the app title
st.title('My First streamlit app')

#streamlit run[filen name].pyrun
#Display text output
st.write('Welcome to my first streamlit app')

#Display a button
st.button("Reset",type="primary")
if st.button("Say Hello"):
   st.write("Why hello there")
else:
   st.write("Goodbye")