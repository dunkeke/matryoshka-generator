"""
Matryoshka Style Wallpaper Generator (v6)
----------------------------------------

This version focuses on faithfully recreating the cosy matryoshka
wallpaper aesthetic seen in the reference pictures. It adds explicit
style guardrails (grainy paper texture, soft pastels, flat shapes,
minimal shading, no outlines, repeating pattern) and more controlled
facial/body options. The prompt builder now assembles a strict style
recipe plus scene details, and the app can call an ``imagegen`` backend
if it is available in the environment.
"""

import importlib
import importlib.util
from textwrap import dedent

import streamlit as st

STYLE_RECIPE = dedent(
    """
    Strict style recipe:
    - cosy vintage children's-book wallpaper, handmade paper texture with fine visible grain
    - flat colour fills, no hard outlines, no gradients, almost no shading
    - rounded matryoshka silhouettes with softly curved bases and flat circular faces
    - tiny dot or curved-line eyes, small coloured mouth, rosy cheeks, no nose
    - limited pastel/earthy palette, low contrast, matte finish
    - simple scattered motifs (trees, mushrooms, leaves, books, mugs, snowflakes)
    - repeating pattern layout with generous spacing, calm and uncluttered
    """
)


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
    pattern_density: str,
    texture_strength: str,
) -> str:
    """Compose a strict prompt that locks in the matryoshka wallpaper style."""
    if secondary_subject and secondary_subject.lower() not in {"none", ""}:
        subjects = f"{primary_subject} and {secondary_subject} figures"
    else:
        subjects = f"{primary_subject} figures"

    face_text = (
        f"They have round plump faces with a head-to-body ratio of {head_body_ratio}, "
        "no noses, "
        f"tiny {eye_style} eyes and small {mouth_color} mouths with soft blush cheeks."
    )
    flat_text = (
        " Faces are perfectly flat circles and bodies have smoothly curved bases for a natural transition."
        if apply_flat_faces
        else ""
    )

    objects_text = ""
    cleaned_objects = [obj.strip() for obj in held_objects.split(",") if obj.strip()]
    if cleaned_objects:
        if len(cleaned_objects) == 1:
            objects_list = cleaned_objects[0]
        else:
            objects_list = ", ".join(cleaned_objects[:-1]) + " and " + cleaned_objects[-1]
        objects_text = f" Each figure holds one of the following props: {objects_list}."

    prompt = (
        "A vertical repeating wallpaper illustration that matches the reference matryoshka images.\n\n"
        f"{STYLE_RECIPE}\n\n"
        f"Scene: repeating, rounded {subjects} {scene_description}. {face_text}{flat_text}{objects_text}\n\n"
        f"Background: soft {background_color} with scattered, simple {background_elements}; pattern density: {pattern_density}.\n\n"
        f"Palette: {palette}; texture intensity: {texture_strength}; finish is grainy, soft, and matte."
    )
    return prompt


def generate_image(prompt: str):
    """Generate an image using the optional ``imagegen`` helper if installed."""

    spec = importlib.util.find_spec("imagegen")
    if spec is None:
        return None, "Image generation not configured: install or provide an `imagegen` module with `make_image()`."

    imagegen = importlib.import_module("imagegen")
    if not hasattr(imagegen, "make_image"):
        return None, "`imagegen` module found but missing `make_image` function."

    try:
        image_path = imagegen.make_image(prompt=prompt)
    except Exception as error:  # noqa: BLE001 - surface generator errors to the UI
        return None, f"Image generation failed: {error}"

    return image_path, None


def main() -> None:
    st.set_page_config(page_title="Matryoshka Wallpaper Generator v6", layout="centered")
    st.title("Matryoshka Style Wallpaper Generator – Style Lock Edition")
    st.markdown(
        "严格复刻参考图的套娃壁纸风格：柔和纸纹理、粉彩低对比、扁平色块、重复排布、微笑脸。选择细节生成稳定的 prompt，并可调用 imagegen 生成图片。"
    )

    with st.form(key="v6_form"):
        primary_subject = st.text_input("Primary subject", value="matryoshka dolls")
        secondary_subject = st.text_input("Secondary subject", value="forest animals")
        scene_description = st.text_input("Scene description", value="sharing tea and reading in a quiet forest")
        background_color = st.text_input("Background colour tone", value="powder blue")
        background_elements = st.text_input(
            "Background elements", value="evergreen trees, mushrooms, leaves, berries, tiny stars, books"
        )
        palette = st.text_input(
            "Overall colour palette", value="pastel blues, warm creams, moss greens, muted browns, blush pink"
        )
        head_body_ratio = st.text_input("Head-to-body ratio (smaller head)", value="1:1.3")
        apply_flat_faces = st.checkbox(
            "Use flat round faces with smoothly curved bases", value=True
        )
        mouth_color = st.text_input("Mouth colour", value="soft red")
        eye_style = st.selectbox(
            "Eye style", options=["dot", "curved line"], index=0
        )
        held_objects = st.text_input(
            "Objects held by figures (comma-separated)",
            value="lantern, book, wrapped gift, holly and berries, mug",
        )
        pattern_density = st.selectbox(
            "Pattern density", options=["spacious", "balanced", "dense"], index=1
        )
        texture_strength = st.selectbox(
            "Paper texture strength", options=["subtle", "medium", "pronounced"], index=1
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
            pattern_density.strip(),
            texture_strength.strip(),
        )
        st.subheader("Generated Prompt")
        st.code(prompt)

        image_path, error = generate_image(prompt)
        if image_path:
            st.subheader("Generated Image")
            st.image(image_path)
        elif error:
            st.info(error)


if __name__ == "__main__":
    main()
