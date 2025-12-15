"""
Matryoshka Style Wallpaper Generator (v6)
----------------------------------------

This version adds customization for mouth colour and eye style,
addressing the latest feedback.  Users can specify a mouth colour
(e.g. red) and choose between small dot eyes or gentle curved lines
for the eyes.  The head-to-body ratio can be adjusted to make the
head smaller relative to the body (e.g. 1:1.3), and the flat face and
curved base options remain available.  The prompt builder
incorporates these selections into the descriptive text, ensuring
consistent output style.

To generate images, integrate your favourite image generator into the
``generate_image`` function.
"""

import streamlit as st

def build_prompt(
    primary_subject: str,
    secondary_subject: str,
    scene_description: str,
    background_color: str,
    background_elements: str,
    palette: str,
    head_body_ratio: str,
    apply_flat_faces: bool,
    mouth_color: str,
    eye_style: str,
    held_objects: str,
) -> str:
    """Compose the prompt with mouth colour and eye style options."""
    if secondary_subject and secondary_subject.lower() not in {"none", ""}:
        subjects = f"{primary_subject} and {secondary_subject} figures"
    else:
        subjects = f"{primary_subject} figures"

    # facial features text
    face_text = (
        f" They have round plump faces with a head-to-body ratio of {head_body_ratio}, "
        "no noses, "
        f"small {eye_style} eyes and small {mouth_color} mouths."
    )
    flat_text = ""
    if apply_flat_faces:
        flat_text = (
            " Their faces are flat and circular, and their bases are smoothly curved "
            "for a natural transition to the body."
        )

    objects_text = ""
    cleaned_objects = [obj.strip() for obj in held_objects.split(",") if obj.strip()]
    if cleaned_objects:
        if len(cleaned_objects) == 1:
            objects_list = cleaned_objects[0]
        else:
            objects_list = ", ".join(cleaned_objects[:-1]) + " and " + cleaned_objects[-1]
        objects_text = f" Each figure holds one of the following objects: {objects_list}."

    prompt = (
        "A vertical wallpaper illustration in a cozy, textured, minimalist "
        "folk-art style, resembling risograph or colored pencil on grainy paper, "
        "matching the aesthetic of the reference images.\n\n"
        f"The scene includes repeating, rounded {subjects} {scene_description}."
        f"{face_text}{flat_text}{objects_text}\n\n"
        f"The background is a soft {background_color} filled with scattered, simple "
        f"{background_elements}.\n\n"
        f"The overall color palette is {palette}, and the texture is grainy, soft, and matte."
    )
    return prompt

def generate_image(prompt: str):
    return None

def main() -> None:
    st.set_page_config(page_title="Matryoshka Wallpaper Generator v6", layout="centered")
    st.title("Matryoshka Style Wallpaper Generator – Mouth & Eye Edition")
    st.markdown(
        "Customise the mouth colour and eye style of your matryoshka figures, "
        "tweak the head-to-body ratio for a smaller head, and choose whether to "
        "apply flat faces with curved bases.  Combine this with object holding "
        "and background settings to craft your perfect prompt."
    )
    with st.form(key="v6_form"):
        primary_subject = st.text_input("Primary subject", value="matryoshka dolls")
        secondary_subject = st.text_input("Secondary subject", value="none")
        scene_description = st.text_input("Scene description", value="doing different cosy activities")
        background_color = st.text_input("Background colour tone", value="pastel blue")
        background_elements = st.text_input(
            "Background elements", value="mushrooms, evergreen trees, stars, books, leaves and berries"
        )
        palette = st.text_input(
            "Overall colour palette", value="pastel blues, warm creams, earthy greens and browns"
        )
        head_body_ratio = st.text_input("Head-to-body ratio (smaller head)", value="1:1.3")
        apply_flat_faces = st.checkbox(
            "Use flat round faces with smoothly curved bases", value=True
        )
        mouth_color = st.text_input("Mouth colour", value="red")
        eye_style = st.selectbox(
            "Eye style", options=["dot", "curved line"], index=0
        )
        held_objects = st.text_input(
            "Objects held by figures (comma-separated)",
            value="lantern, book, wrapped gift, holly and berries, mug",
        )
        submit = st.form_submit_button("Generate Prompt")

    if submit:
        prompt = build_prompt(
            primary_subject.strip(),
            secondary_subject.strip(),
            scene_description.strip(),
            background_color.strip(),
            background_elements.strip(),
            palette.strip(),
            head_body_ratio.strip(),
            apply_flat_faces,
            mouth_color.strip(),
            eye_style.strip(),
            held_objects.strip(),
        )
        st.subheader("Generated Prompt")
        st.write(prompt)
        image_path = generate_image(prompt)
        if image_path:
            st.subheader("Generated Image")
            st.image(image_path)
        else:
            st.info(
                "Image generation is not configured. Use the prompt above with your own generator or integrate it here."
            )

if __name__ == "__main__":
    main()