"""
Matryoshka Style Wallpaper Generator
------------------------------------

This Streamlit application provides an interactive interface for generating
customised prompts in the style of the supplied matryoshka (nesting doll)
wallpaper illustrations.  Users can specify the main subject, facial
details, actions, background colour, background motifs, and overall
colour palette.  The app will assemble these choices into a single
description following the prompt template provided by the user.

While the application demonstrates how to construct the prompt, it does
not directly generate an image in this environment.  To enable image
generation, integrate your preferred image generation service (for
example, the ``imagegen.make_image`` tool available in this notebook
environment or an external API) within the ``generate_image`` function.
"""

import streamlit as st

def build_prompt(
    subject: str,
    face_details: str,
    actions: str,
    background_color: str,
    background_elements: str,
    palette: str,
) -> str:
    """Construct the descriptive prompt based on user selections.

    Args:
        subject: The main subject (e.g. "cat", "bear", "astronaut").
        face_details: Details about the facial expression or features
            (e.g. "closed smiling eyes", "simple dot eyes").
        actions: What the figures are doing or wearing
            (e.g. "wearing cozy sweaters", "holding small plants").
        background_color: The overall tone of the background colour
            (e.g. "muted green", "warm cream").
        background_elements: The motifs that appear scattered across
            the background (e.g. "leaves and flowers", "stars and planets").
        palette: A description of the overall colour palette
            (e.g. "earthy tones", "pastel colours").

    Returns:
        A string representing the full descriptive prompt.
    """

    prompt = (
        "A vertical wallpaper illustration in a cozy, textured, minimalist "
        "folk-art style, resembling risograph or colored pencil on grainy "
        "paper, matching the aesthetic of image_0.png, image_1.png, and "
        "image_2.png.\n\n"
        f"The main subjects are repeating, rounded {subject} figures, "
        "designed specifically in the shape of matryoshka dolls (nesting "
        "dolls). They have simple, happy faces with rosy cheeks and "
        f"{face_details}.\n\n"
        f"They are {actions}.\n\n"
        f"The background is a soft {background_color} filled with scattered, "
        f"simple {background_elements}.\n\n"
        f"The overall color palette is {palette}, and the texture is "
        "grainy, soft, and matte."
    )
    return prompt

def generate_image(prompt: str):
    """Placeholder for image generation logic.

    In this demo, the function only returns ``None`` because no image
    generation API is connected.  If you wish to enable image
    generation, integrate a call to your preferred image generation
    service here.  For example, with the ``imagegen`` tool provided in
    this environment, you could import it and call:

    ````python
    from imagegen import make_image
    image_path = make_image(prompt=prompt)
    return image_path
    ````

    Args:
        prompt: The descriptive prompt produced by ``build_prompt``.

    Returns:
        ``None`` in this default implementation.  Replace with a path
        or ``PIL.Image`` object to display an image using Streamlit.
    """
    # TODO: integrate with image generation service
    return None

def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(page_title="Matryoshka Style Wallpaper Generator", layout="centered")
    st.title("Matryoshka Style Wallpaper Generator")
    st.markdown(
        "This interactive app lets you assemble a prompt in the style of the "
        "provided matryoshka wallpapers.  Fill in the fields below to "
        "customise your design, then click **Generate** to produce the prompt "
        "(and optionally an image, if you integrate an image generation service)."
    )
    with st.form(key="prompt_form"):
        subject = st.text_input(
            "Main subject (e.g., cat / bear / astronaut)", value="cat"
        )
        face_details = st.text_input(
            "Facial details (e.g., closed smiling eyes / simple dot eyes)",
            value="closed smiling eyes",
        )
        actions = st.text_input(
            "Actions or state (e.g., wearing cozy sweaters / holding small plants / sleeping)",
            value="wearing cozy sweaters",
        )
        background_color = st.text_input(
            "Background colour tone (e.g., muted green / warm cream)", value="muted green"
        )
        background_elements = st.text_input(
            "Background elements (e.g., leaves and flowers / stars and planets / tiny houses)",
            value="leaves and flowers",
        )
        palette = st.text_input(
            "Overall colour palette (e.g., earthy tones / pastel colours / monochromatic blue)",
            value="earthy tones",
        )
        generate = st.form_submit_button("Generate")

    if generate:
        prompt = build_prompt(
            subject.strip(),
            face_details.strip(),
            actions.strip(),
            background_color.strip(),
            background_elements.strip(),
            palette.strip(),
        )
        st.subheader("Generated Prompt")
        st.write(prompt)

        # Attempt image generation if possible
        image_path = generate_image(prompt)
        if image_path:
            st.subheader("Generated Image")
            st.image(image_path)
        else:
            st.info(
                "Image generation is not configured in this environment.  "
                "The prompt above can be used with your own image generation "
                "service or the `imagegen` tool available in this notebook."
            )

if __name__ == "__main__":
    main()