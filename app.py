import cohere
import streamlit as st
import os
import textwrap

# Cohere API key
api_key = os.environ["CO_KEY"]

# Set up Cohere client
co = cohere.Client(api_key)

def generate_idea(industry, temperature):
  """
  Generate startup idea given an industry name
  Arguments:
    industry(str): the industry name
    temperature(str): the Generate model `temperature` value
  Returns:
    response(str): the startup idea
  """
  base_idea_prompt = textwrap.dedent("""
  Generate a movie idea based on the title of two movies seperated by the words meets.
###
Jaws Meets Twister
###
A group of scientists are investigating a mysterious phenomenon that is causing massive destruction in the ocean. As they investigate, they discover that it is a giant, man-eating shark that is responsible for the destruction. They must race against time to stop the shark before it destroys the entire ocean via the world's greatest megastorm a tornado on the water!
###
Santa Claus Meets Nightmare on ElmStreet
###
The story of Santa Claus, the legendary figure who brings joy to children around the world, meets the horror of the Nightmare on Elm Street. Santa Claus is a kind and gentle man who is always looking out for the best interests of children. He is a protector and a guardian, and he will do anything to keep the children of the world safe. However, when Santa Claus comes face to face with the nightmare of the Elm Street, he must confront his own fears and fight for the children he has vowed to protect.
###
Top Gun Meets Transformers
###
The story of Top Gun, the iconic 80s movie about a group of young pilots, meets the world of the Transformers. The Top Gun program has been reactivated and a new group of young pilots are being trained to take on the latest threat to America's national security: the Decepticons. The Top Gun pilots must learn to work together and use their skills to take down the Decepticons and protect America from destruction.
###
Super Mario Brothers meets Ant Man
###
The story of the Super Mario Brothers, the classic video game about two plumbers who must save the Mushroom Kingdom from the evil Bowser, meets the world of Ant Man. The Super Mario Brothers are back and they must once again save the Mushroom Kingdom from the evil Bowser. However, this time they are joined by Ant Man, the tiny hero who can shrink down to the size of an ant and use his super strength to take on even the biggest of enemies. Together, the Super Mario Brothers and Ant Man must work together to defeat Bowser and save the Mushroom Kingdom once and for all.
###""")

  # Call the Cohere Generate endpoint
  response = co.generate( 
    model='command-xlarge-nightly', 
    prompt = base_idea_prompt + " " + industry + "\n:",
    max_tokens=50, 
    temperature=temperature,
    k=0, 
    p=0.7, 
    frequency_penalty=0.1, 
    presence_penalty=0, 
    stop_sequences=["--"])
  startup_idea = response.generations[0].text
  startup_idea = startup_idea.replace("\n\n--","").replace("\n--","").strip()

  return startup_idea

'''def generate_name(idea, temperature):
  """
  Generate startup name given a startup idea
  Arguments:
    idea(str): the startup idea
    temperature(str): the Generate model `temperature` value
  Returns:
    response(str): the startup name
  """
  base_name_prompt= textwrap.dedent("""
    This program generates a startup name and name given the startup idea.

    Startup Idea: A platform that generates slide deck contents automatically based on a given outline
    Startup Name: Deckerize

    --
    Startup Idea: An app that calculates the best position of your indoor plants for your apartment
    Startup Name: Planteasy 

    --
    Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting a whole week
    Startup Name: Hearspan

    --
    Startup Idea: An online primary school that lets students mix and match their own curriculum based on their interests and goals
    Startup Name: Prime Age

    --
    Startup Idea:""")'''
'''
  # Call the Cohere Generate endpoint
  response = co.generate( 
    model='xlarge', 
    prompt = base_name_prompt + " " + idea + "\nStartup Name:",
    max_tokens=10, 
    temperature=temperature,
    k=0, 
    p=0.7, 
    frequency_penalty=0, 
    presence_penalty=0, 
    stop_sequences=["--"])
  startup_name = response.generations[0].text
  startup_name = startup_name.replace("\n\n--","").replace("\n--","").strip()

  return startup_name '''

# The front end code starts here

st.title("🎥 Startup Idea Generator")

form = st.form(key="user_settings")
with form:
  st.write("Pick Two Movie Titles and Enter them as X meets Y to [i.e Jaws Meets Twister] Receive a World Class Plot Idea  ")
  # User input - X Meets Y Title
  industry_input = st.text_input("Industry", key = "industry_input")

  # Create a two-column view
  col1, col2 = st.columns(2)
  with col1:
      # User input - The number of ideas to generate
      num_input = st.slider(
        "Number of ideas", 
        value = 3, 
        key = "num_input", 
        min_value=1, 
        max_value=10,
        help="Choose to generate between 1 to 10 ideas")
  with col2:
      # User input - The 'temperature' value representing the level of creativity
      creativity_input = st.slider(
        "Creativity", value = 0.5, 
        key = "creativity_input", 
        min_value=0.1, 
        max_value=0.9,
        help="Lower values generate more “predictable” output, higher values generate more “creative” output")  
  # Submit button to start generating ideas
  generate_button = form.form_submit_button("Generate Idea")

  if generate_button:
    if industry_input == "":
      st.error("Industry field cannot be blank")
    else:
      my_bar = st.progress(0.05)
      st.subheader("Startup Ideas:")

      for i in range(num_input):
          st.markdown("""---""")
          startup_idea = generate_idea(industry_input,creativity_input)
         # startup_name = generate_name(startup_idea,creativity_input)
        #  st.markdown("##### " + startup_name)
          st.write(startup_idea)
          my_bar.progress((i+1)/num_input)