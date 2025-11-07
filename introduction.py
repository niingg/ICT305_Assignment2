"""
introduction.py - Interactive Human Body Diagram for Diabetes Education
VERSION: Base64 Embedded Images (No File Path Issues)

This version converts images to base64 so they work everywhere in Streamlit.
"""

import plotly.graph_objects as go
import streamlit as st
import os
import base64


def image_to_base64(image_path):
    """
    Convert an image file to base64 string for embedding in Plotly.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        str: Base64 encoded image URI
    """
    try:
        with open(image_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            # Determine file extension
            if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
                return f"data:image/jpeg;base64,{img_data}"
            elif image_path.lower().endswith('.png'):
                return f"data:image/png;base64,{img_data}"
    except FileNotFoundError:
        print(f"Warning: Image file not found: {image_path}")
        return None


def get_image_path(filename):
    """
    Get the full path to an image file.
    Checks multiple possible locations.
    
    Args:
        filename (str): Name of the image file
        
    Returns:
        str: Full path to image file or None if not found
    """
    possible_paths = [
        filename,
        os.path.join(os.path.dirname(__file__), filename),
        os.path.join('images', filename),
        os.path.join(os.path.dirname(__file__), 'images', filename),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return os.path.abspath(path)
    
    return None


def create_body_diagram():
    """
    Create an interactive human body diagram showing how diabetes affects different organs.
    Uses base64 embedded images for reliable display in Streamlit.
    
    Returns:
        plotly.graph_objects.Figure: Interactive body diagram
    """
    
    # Creating the base figure
    fig = go.Figure()

    # Get image paths and convert to base64
    print("Loading images...")
    
    # Base body
    base_body_path = get_image_path("base_body.jpg")
    if base_body_path:
        base_body_b64 = image_to_base64(base_body_path)
        if base_body_b64:
            fig.add_layout_image(
                source=base_body_b64,
                x=0.273, y=1, sizex=1, sizey=1,
                xref="paper", yref="paper",
                layer="below"
            )

    # Arteries 1
    arteries_path = get_image_path("arteriess.png")
    if arteries_path:
        arteries_b64 = image_to_base64(arteries_path)
        if arteries_b64:
            fig.add_layout_image(
                source=arteries_b64,
                x=0.255, y=0.83, sizex=0.8, sizey=0.7,
                xref="paper", yref="paper",
                layer="above",
                opacity=0.2
            )

    # Pancreas 2
    pancreas_path = get_image_path("pancreas.png")
    if pancreas_path:
        pancreas_b64 = image_to_base64(pancreas_path)
        if pancreas_b64:
            fig.add_layout_image(
                source=pancreas_b64,
                x=0.361, y=0.60, sizex=0.09, sizey=0.09,
                xref="paper", yref="paper",
                layer="below",
                opacity=0.2
            )
    
    # Left Kidney 3
    left_kidney_path = get_image_path("leftkidney.png")
    if left_kidney_path:
        left_kidney_b64 = image_to_base64(left_kidney_path)
        if left_kidney_b64:
            fig.add_layout_image(
                source=left_kidney_b64,
                x=0.345, y=0.61, sizex=0.08, sizey=0.08,
                xref="paper", yref="paper",
                layer="below",
                opacity=0.2
            )

    # Right Kidney 4
    right_kidney_path = get_image_path("rightkidney.png")
    if right_kidney_path:
        right_kidney_b64 = image_to_base64(right_kidney_path)
        if right_kidney_b64:
            fig.add_layout_image(
                source=right_kidney_b64,
                x=0.395, y=0.61, sizex=0.08, sizey=0.08,
                xref="paper", yref="paper",
                layer="below",
                opacity=0.2
            )

    # Stomach 5
    stomach_path = get_image_path("stomach.png")
    if stomach_path:
        stomach_b64 = image_to_base64(stomach_path)
        if stomach_b64:
            fig.add_layout_image(
                source=stomach_b64,
                x=0.338, y=0.70, sizex=0.16, sizey=0.16,
                xref="paper", yref="paper",
                layer="above",
                opacity=0.2
            )

    # Liver 6
    liver_path = get_image_path("liver.png")
    if liver_path:
        liver_b64 = image_to_base64(liver_path)
        if liver_b64:
            fig.add_layout_image(
                source=liver_b64,
                x=0.33, y=0.70, sizex=0.16, sizey=0.16,
                xref="paper", yref="paper",
                layer="above",
                opacity=0.2
            )

    # Heart 7
    heart_path = get_image_path("heart.png")
    if heart_path:
        heart_b64 = image_to_base64(heart_path)
        if heart_b64:
            fig.add_layout_image(
                source=heart_b64,
                x=0.35, y=0.78, sizex=0.17, sizey=0.13,
                xref="paper", yref="paper",
                layer="above",
                opacity=0.2
            )

    # Lungs 8 
    lungs_path = get_image_path("lungs.png")
    if lungs_path:
        lungs_b64 = image_to_base64(lungs_path)
        if lungs_b64:
            fig.add_layout_image(
                source=lungs_b64,
                x=0.33, y=0.85, sizex=0.22, sizey=0.22,
                xref="paper", yref="paper",
                layer="above",
                opacity=0.2
            )

    # Brain 9
    brain_path = get_image_path("brain.png")
    if brain_path:
        brain_b64 = image_to_base64(brain_path)
        if brain_b64:
            fig.add_layout_image(
                source=brain_b64,
                x=0.344, y=1.02, sizex=0.15, sizey=0.15,
                xref="paper", yref="paper",
                layer="above",
                opacity=0.2
            )

    print("Images loaded successfully!")

    # Stores all the Hover data
    hover_data = [
        # Hover for Brain
        {
            'name': 'Brain', 
            'x': 2.2, 
            'y': 19, 
            'info': 'Controls the nervous system',
            'affected_by': 'Stroke, High BP, Mental Health, High Cholesterol, and Heavy Alcohol Consumptions', 
            'index': 9
        },
        # Hover for Heart
        {
            'name': 'Heart', 
            'x': 2.2, 
            'y': 14, 
            'info': 'Pumps blood',
            'affected_by': 'High Cholesterol, High BP, Stroke, Smoker, and Heart Disease or Attack',
            'index': 7
        },
        # Hover for Liver
        {
            'name': 'Liver', 
            'x': 2.1, 
            'y': 13, 
            'info': 'Filters blood', 
            'affected_by': 'High Cholesterol and Heavy Alcohol Consumptions',
            'index': 6
        },
        # Hover for Pancreas
        {
            'name': 'Pancreas', 
            'x': 2.2, 
            'y': 11.5,
            'info': 'Produces insulin', 
            'affected_by': 'Heavy Alcohol Consumptions',
            'index': 2
        },
        # Hover for Left Kidney
        {
            'name': 'Left Kidney', 
            'x': 2.1, 
            'y': 11.3, 
            'info': 'Filter blood', 
            'affected_by': 'High BP, Heavy Alcohol Consumptions',
            'index': 3
        },
        # Hover for Right Kidney
        {
            'name': 'Right Kidney', 
            'x': 2.25, 
            'y': 11.3, 
            'info': 'Filter blood', 
            'affected_by': 'High BP, Heavy Alcohol Consumptions',
            'index': 4
        },
        # Hover for Stomach
        {
            'name': 'Stomach', 
            'x': 2.2, 
            'y': 12.5, 
            'info': 'Digests Food', 
            'affected_by': '-', 
            'index': 5
        },
        # Hover for Lungs
        {
            'name': 'Lungs', 
            'x': 2.2, 
            'y': 15,
            'info': 'Oxygen exchange',
            'affected_by': 'Smoker',
            'index': 8
        },
        # Hover for Arteries (Plotted 3 times so user can find them easily!)
        {
            'name': 'Arteries', 
            'x': 2.5, 
            'y': 12,
            'info': 'Carries Oxygen to the body',
            'affected_by': 'High Cholesterol, High BP, Stroke, and Heart Disease or Attack',
            'index': 1
        },
        {
            'name': 'Arteries', 
            'x': 2.35, 
            'y': 16,
            'info': 'Carries Oxygen to the body',
            'affected_by': 'High Cholesterol, High BP, Stroke, and Heart Disease or Attack',
            'index': 1
        },
        {
            'name': 'Arteries', 
            'x': 2.3, 
            'y': 8,
            'info': 'Carries Oxygen to the body',
            'affected_by': 'High Cholesterol, High BP, Stroke, and Heart Disease or Attack',
            'index': 1
        }
    ]

    # Creating for loop for the hover tooltips
    for organ in hover_data:
        fig.add_trace(go.Scatter(
            x=[organ['x']],
            y=[organ['y']],
            mode='markers',
            marker=dict(size=30, opacity=0),  # Opacity is 0 because scatter plot is hidden
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>'
                '<br>'
                '%{customdata[1]}<br>'
                'Affected by: %{customdata[2]}'
                '<extra></extra>'
            ),
            customdata=[[organ['name'], organ['info'], organ['affected_by']]],
            hoverlabel=dict(
                font= dict(color='black'),
                bgcolor="#EEC8A3",
                bordercolor="#931A23"),
            showlegend=False,
            visible=False
        ))

    # Define conditions and affected organs
    conditions = {
        'None': [0],  # none
        'Show All': [1, 2, 3, 4, 5, 6, 7, 8, 9],  # all organs
        'High Cholesterol': [1, 6, 7, 9],  # arteries, liver, heart, brain
        'High Blood Pressure': [1, 7, 9, 3, 4],  # arteries, heart, brain, kidneys
        'Heavy Alcohol Consumptions': [2, 3, 4, 6, 9],  # pancreas, kidneys, liver, brain
        'Mental Health': [9],  # brain
        'Stroke': [9, 7, 1],  # brain, heart, arteries
        'Heart Disease or Attack': [7, 1],  # heart, arteries
        'Smoker': [7, 8],  # lungs, heart
    }

    # Create dropdown buttons
    dropdown_buttons = []

    for condition_name, organ_indices in conditions.items():
        update_dict = {}
        
        # Gray out all organs or highlight based on selection
        for i in range(1, 10):
            if i in organ_indices:
                update_dict[f'images[{i}].opacity'] = 1.0  # Highlight
            else:
                update_dict[f'images[{i}].opacity'] = 0.3  # Gray out
        
        visible_traces = []
        for organ in hover_data:
            if organ['index'] in organ_indices:
                visible_traces.append(True)   # Show hover
            else:
                visible_traces.append(False)  # Hide hover
        
        # Create button
        dropdown_buttons.append(
            dict(
                label=condition_name,
                method="update",
                args=[
                    {"visible": visible_traces},  # Update traces (hover)
                    update_dict
                ]
            )
        )

    # Update layout with dropdown
    fig.update_layout(
        xaxis_visible=False,
        yaxis_visible=False,
        dragmode=False,
        plot_bgcolor='white',
        margin=dict(l=50, r=0, t=0, b=0), 
        autosize=True,
        width=None,
        height=None,
        xaxis=dict(range=[1, 4]),   # X-axis range (min, max)
        yaxis=dict(range=[0, 20]),  # Y-axis range (min, max)
        hovermode='closest',
        title={
            'text': 'How Diabetes Affects Your Body',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#931A23'}
        },
        updatemenus=[
            dict(
                buttons=dropdown_buttons,
                direction="down",
                pad={"r": 25, "t": 60},
                showactive=True,
                x=0.3,
                xanchor="right",
                y=1.12,
                yanchor="top",
                bgcolor="white",
                bordercolor="black",
                borderwidth=2,
                font=dict(size=12, color = "black"),
            ),
        ] 
    )

    return fig


def display_body_diagram():
    """
    Display the body diagram in Streamlit.
    This is the function that app.py calls.
    """
    st.write("""
    Diabetes can affect multiple organs and systems in your body. 
    Use the dropdown below to explore which organs are affected by different conditions:
    """)
    
    fig = create_body_diagram()
    st.plotly_chart(fig, use_container_width=True , use_container_height=True)
    
    st.info("""
    💡 **Did you know?**
    - Diabetes damages blood vessels over time, affecting organs that rely on good circulation
    - The pancreas is crucial because it produces insulin, which regulates blood sugar
    - High blood pressure and high cholesterol often occur together with diabetes, 
      compounding organ damage
    - Regular check-ups and lifestyle changes can help prevent or delay these complications
    """)


if __name__ == "__main__":
    """
    Standalone execution - displays the diagram directly
    """
    fig = create_body_diagram()
    fig.show()