"""
conclusion.py - Sankey Diagram for Diabetes Analysis Summary
This module creates a Sankey diagram showing the flow of data through hypotheses
and their conclusions (Accept/Reject).
"""

import plotly.graph_objects as go


def create_sankey_diagram():
    """
    Create and return a Sankey diagram showing hypothesis flow and conclusions.
    
    Returns:
        plotly.graph_objects.Figure: Sankey diagram figure
    """
    
    nodes = [
        # Data inputs 0-17
        "Fruits", "Veggies", "Smoker", "Heavy Alcohol Consumption", "Any Healthcare Cost", 
        "Any Doctor Cost", "Stroke", "Education", "Diabetes or No", "Income",
        "Previous case of Heart Attack or Disease", "General Health", "Physical Activity",
        "Mental Health", "High Blood Pressure", "High Cholesterol",
        "Physical Health", "Difficulty Walking",
        
        # Hypotheses 18-22
        "Hypothesis 1: Does Bad Habits/Lifestyle increases Diabetes",
        "Hypothesis 2: Preventing Diabetes Through Education",
        "Hypothesis 3: Accessibility to Healthcare", 
        "Hypothesis 4: Self Awareness Impact on Diabetes", 
        "Hypothesis 5: Do Existing Conditions Predict Diabetes?",
        
        # Accept and Reject 23-24
        "✓ Contribute to Diabetes", "✗ Does Not Contribute to Diabetes"
    ]

    sources = [
        0,0, # Fruits
        1,1, # Veggies
        2,2, # Smoker
        3,3, # Heavy Alcohol Consumption
        4, # Any Healthcare Cost
        5, # Any Doctor Cost
        6, # Stroke
        7, # Education
        8,8,8,8, # Diabetes or No
        9, # Income
        10, # Previous case of Heart Attack or Disease
        11, # General Health
        12,12,12, # Physical Activity
        13, # Mental Health
        14, # High Blood Pressure
        15, # High Cholesterol
        16, # Physical Health
        17, # Difficulty Walking
        18, # Hypothesis 1
        19, # Hypothesis 2
        20, # Hypothesis 3
        21, # Hypothesis 4
        22, # Hypothesis 5
    ]

    targets = [
        18,19, # Fruits to Hypothesis 1 and 2
        18,19, # Veggies to Hypothesis 1 and 2
        18,19, # Smoker to Hypothesis 1 and 2
        18,19, # Heavy Alcohol Consumption to Hypothesis 1 and 2
        20, # Any Healthcare Cost to Hypothesis 3
        20, # Any Doctor Cost to Hypothesis 3
        22, # Stroke to Hypothesis 5
        19, # Education to Hypothesis 2
        18,20,21,22, # Diabetes or No to Hypotheses 1,3,4,5
        20, # Income to Hypothesis 3
        22, # Previous case of Heart Attack or Disease to Hypothesis 5
        21, # General Health to Hypothesis 4
        18,19,21, # Physical Activity to Hypotheses 1,2,4
        21, # Mental Health to Hypothesis 4
        22, # High Blood Pressure to Hypothesis 5
        22, # High Cholesterol to Hypothesis 5
        21, # Physical Health to Hypothesis 4
        21, # Difficulty Walking to Hypothesis 4    
        23, # Hypothesis 1 to Accept (Contribute)
        23, # Hypothesis 2 to Accept (Contribute)
        24, # Hypothesis 3 to Reject (Does Not Contribute)
        23, # Hypothesis 4 to Accept (Contribute)
        23, # Hypothesis 5 to Accept (Contribute)
    ]

    values = [
        100,100,
        100,100,
        100,100,
        100,100,
        200,
        200,
        200,
        200,
        50,50,50,50,
        200,
        200,
        200,
        66,66,66,
        200, 
        200,
        200,
        200,
        200,
        400,
        400,
        400,
        400,
        400, 
    ]

    # Create color scheme
    node_colors = [
        # Data inputs 0-17 (shades of red/brown)
        "#D21502", "#A91B0D", "#4C0805", "#BC5449",  
        "#7E2811", '#900603', '#670C07',              
        "#9C1003", "#791812", "#600B04", "#420D09",
        "#AC5444", "#A8565A", "#6B3939", "#75120B",  
        "#990F02", "#B80F0A", "#5E1914",              
        
        # Hypotheses 18-22 (warm tones)
        '#FFF1A4','#DD9C7C','#EEC8A3','#D24C49','#931A23',  

        # Accept and Reject 23-24
        "#738a6e",  # Green for Accept
        "#9B1128"   # Red for Reject
    ]
    
    link_colors = [
        'rgba(255,241,164,0.7)','rgba(221,156,124,0.7)', # Fruits to Hypothesis 1 and 2
        'rgba(255,241,164,0.7)','rgba(221,156,124,0.7)', # Veggies to Hypothesis 1 and 2
        'rgba(255,241,164,0.7)','rgba(221,156,124,0.7)', # Smoker to Hypothesis 1 and 2
        'rgba(255,241,164,0.7)','rgba(221,156,124,0.7)', # Heavy Alcohol Consumption to Hypothesis 1 and 2
        'rgba(238,200,163,0.7)',  # Any Healthcare Cost to Hypothesis 3
        'rgba(238,200,163,0.7)', # Any Doctor Cost to Hypothesis 3
        'rgba(147,26,35,0.7)', # Stroke to Hypothesis 5
        'rgba(221,156,124,0.7)', # Education to Hypothesis 2
        'rgba(255,241,164,0.7)','rgba(238,200,163,0.7)', 'rgba(210,76,73,0.7)','rgba(147,26,35,0.7)', # Diabetes or No to Hypotheses 1,3,4,5
        'rgba(238,200,163,0.7)', # Income to Hypothesis 3
        'rgba(147,26,35,0.7)', # Previous case of Heart Attack or Disease to Hypothesis 5
        'rgba(210,76,73,0.7)', # General Health to Hypothesis 4
        'rgba(255,241,164,0.7)','rgba(221,156,124,0.7)','rgba(210,76,73,0.7)', # Physical Activity to Hypotheses 1,2,4
        'rgba(210,76,73,0.7)', # Mental Health to Hypothesis 4
        'rgba(147,26,35,0.7)', # High Blood Pressure to Hypothesis 5
        'rgba(147,26,35,0.7)', # High Cholesterol to Hypothesis 5
        'rgba(210,76,73,0.7)', # Physical Health to Hypothesis 4
        'rgba(210,76,73,0.7)', # Difficulty Walking to Hypothesis 4    
        'rgba(115,138,110,1)', # Hypothesis 1 to Accept
        'rgba(115,138,110,1)', # Hypothesis 2 to Accept
        'rgba(155,17,40,1)', # Hypothesis 3 to Reject
        'rgba(115,138,110,1)', # Hypothesis 4 to Accept
        'rgba(115,138,110,1)' # Hypothesis 5 to Accept
    ]

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        # Define the nodes
        node=dict(
            pad=15,                    # Spacing between nodes
            thickness=50,
            label=nodes,               # Node labels
            color=node_colors,         # Node colors
            hovertemplate="%{label}<extra></extra>",  # Clean hover text
            
        ),
        # Define the links (flows)
        link=dict(
            source=sources,            # Starting node indices
            target=targets,            # Ending node indices
            value=values,              # Flow magnitudes
            color=link_colors,         # Link colors
            hovertemplate="%{source.label} → %{target.label}<extra></extra>"
        )
    )])
    
    # Update layout for better appearance
    fig.update_layout(
    font=dict(
        size=14, 
        color="#000000", 
        family="Arial"  
    ),
    
    paper_bgcolor="#F8F9FA",  
    plot_bgcolor="#F8F9FA",   
    height=700,               
    margin=dict(l=20, r=20, t=80, b=20)  
    )
    
    return fig


if __name__ == "__main__":
    """
    Example usage - run standalone to view the diagram
    """
    fig = create_sankey_diagram()
    fig.show()