import streamlit as st
from PIL import Image, ImageDraw
import random
import pandas as pd
from io import BytesIO

# ----------------------------------
# SIMPLE RULE-BASED DETECTOR (NO ML)
# ----------------------------------
def detect_violation(image):
    width, height = image.size

    x1 = random.randint(10, width//3)
    y1 = random.randint(10, height//3)
    x2 = x1 + random.randint(80, width//2)
    y2 = y1 + random.randint(80, height//2)

    violation_types = [
        "No Helmet",
        "Triple Riding",
        "Signal Jump",
        "Red Light Violation",
        "Wrong Lane Driving"
    ]
    violation = random.choice(violation_types)

    # Suggested fine amounts
    fine_table = {
        "No Helmet": 1000,
        "Triple Riding": 1500,
        "Signal Jump": 2000,
        "Red Light Violation": 2500,
        "Wrong Lane Driving": 1200
    }

    fine_amount = fine_table[violation]

    return (x1, y1, x2, y2), violation, fine_amount


def draw_box(image, box, label):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    draw.rectangle(box, outline="red", width=4)
    draw.text((box[0], box[1] - 12), label, fill="red")
    return img

# ----------------------------------
# STREAMLIT SETTINGS
# ----------------------------------
st.set_page_config(
    page_title="Traffic Violation Legal Dashboard",
    page_icon="⚖️",
    layout="wide"
)

# Sky-blue theme (legal style)
st.markdown("""
    <style>
        body {
            background-color: #d6ecff;
        }
        .reportview-container {
            background-color: #d6ecff;
        }
        .sidebar .sidebar-content {
            background-color: #99ccff;
        }
        h1, h2, h3 {
            color: #003366;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------
# PAGE TITLE
# ----------------------------------
st.title("⚖️ Traffic Violation Detection – Legal Dashboard")
st.write("Upload one or more images to detect violations, assign fines, and generate a report.")

# ----------------------------------
# FILE UPLOADER
# ----------------------------------
uploaded_files = st.file_uploader("Upload Traffic Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Table to store violation records
records = []

if uploaded_files:
    st.subheader("📂 Uploaded Images")

    for uploaded_file in uploaded_files:
        col1, col2 = st.columns(2)

        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", use_column_width=True)

        # Perform detection
        box, violation_label, auto_fine = detect_violation(image)
        result_img = draw_box(image, box, f"{violation_label}")

        with col2:
            st.image(result_img, caption=f"Detected: {violation_label}", use_column_width=True)

            st.write("### 💰 Fine Amount")
            fine_input = st.number_input(
                "Enter Fine Amount (Auto-suggested applied):",
                min_value=0,
                value=auto_fine,
                key=uploaded_file.name
            )

            # Add to final record
            records.append({
                "File Name": uploaded_file.name,
                "Violation": violation_label,
                "Fine Amount": fine_input
            })

# ----------------------------------
# REPORT TABLE
# ----------------------------------
if records:
    st.subheader("📜 Violation Report Table")
    df = pd.DataFrame(records)
    st.dataframe(df, use_container_width=True)

    # Download Option
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    st.download_button(
        label="📥 Download Report as CSV",
        data=buffer.getvalue(),
        file_name="violation_report.csv",
        mime="text/csv"
    )
