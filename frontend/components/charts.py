import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Union, Optional

def create_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: Union[str, List[str]],
    title: str = None,
    color: str = None,
    orientation: str = 'v',
    barmode: str = 'group',
    text: str = None,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a bar chart using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        x (str): Column name for x-axis
        y (Union[str, List[str]]): Column name(s) for y-axis
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        orientation (str, optional): Bar orientation ('v' for vertical, 'h' for horizontal)
        barmode (str, optional): Bar mode ('group', 'stack', 'relative', 'overlay')
        text (str, optional): Column name for text labels
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create bar chart
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        orientation=orientation,
        barmode=barmode,
        text=text,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        xaxis_title=x,
        yaxis_title=y if isinstance(y, str) else None,
        legend_title=color if color else None,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Update text position
    if text:
        fig.update_traces(textposition='outside')
    
    return fig

def create_line_chart(
    data: pd.DataFrame,
    x: str,
    y: Union[str, List[str]],
    title: str = None,
    color: str = None,
    line_shape: str = 'linear',
    markers: bool = True,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a line chart using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        x (str): Column name for x-axis
        y (Union[str, List[str]]): Column name(s) for y-axis
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        line_shape (str, optional): Line shape ('linear', 'spline', 'hv', 'vh', 'hvh', 'vhv')
        markers (bool, optional): Whether to show markers
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create line chart
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        line_shape=line_shape,
        markers=markers,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        xaxis_title=x,
        yaxis_title=y if isinstance(y, str) else None,
        legend_title=color if color else None,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_pie_chart(
    data: pd.DataFrame,
    names: str,
    values: str,
    title: str = None,
    color: str = None,
    hole: float = 0,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a pie chart using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        names (str): Column name for slice names
        values (str): Column name for slice values
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        hole (float, optional): Size of the hole in the center (0-1)
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create pie chart
    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title,
        color=color,
        hole=hole,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    # Update traces
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig

def create_scatter_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = None,
    color: str = None,
    size: str = None,
    hover_name: str = None,
    trendline: str = None,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a scatter plot using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        x (str): Column name for x-axis
        y (str): Column name for y-axis
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        size (str, optional): Column name for size encoding
        hover_name (str, optional): Column name for hover labels
        trendline (str, optional): Trendline type ('ols', 'lowess')
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create scatter plot
    fig = px.scatter(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        size=size,
        hover_name=hover_name,
        trendline=trendline,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        xaxis_title=x,
        yaxis_title=y,
        legend_title=color if color else None,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_heatmap(
    data: pd.DataFrame,
    title: str = None,
    colorscale: str = 'Blues',
    zmin: float = None,
    zmax: float = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a heatmap using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        title (str, optional): Chart title
        colorscale (str, optional): Colorscale for the heatmap
        zmin (float, optional): Minimum value for the color scale
        zmax (float, optional): Maximum value for the color scale
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale=colorscale,
        zmin=zmin,
        zmax=zmax
    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        title_x=0.5,
        height=height,
        template=template,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_histogram(
    data: pd.DataFrame,
    x: str,
    title: str = None,
    color: str = None,
    nbins: int = 30,
    histnorm: str = None,
    barmode: str = 'overlay',
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a histogram using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        x (str): Column name for x-axis
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        nbins (int, optional): Number of bins
        histnorm (str, optional): Histogram normalization ('percent', 'probability', 'density', 'probability density')
        barmode (str, optional): Bar mode ('overlay', 'stack', 'relative')
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create histogram
    fig = px.histogram(
        data,
        x=x,
        title=title,
        color=color,
        nbins=nbins,
        histnorm=histnorm,
        barmode=barmode,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        xaxis_title=x,
        yaxis_title='Count' if histnorm is None else histnorm.capitalize(),
        legend_title=color if color else None,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_box_plot(
    data: pd.DataFrame,
    x: str = None,
    y: str = None,
    title: str = None,
    color: str = None,
    points: str = 'outliers',
    notched: bool = False,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a box plot using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        x (str, optional): Column name for x-axis
        y (str, optional): Column name for y-axis
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        points (str, optional): Display points ('all', 'outliers', 'suspectedoutliers', False)
        notched (bool, optional): Whether to show notched boxes
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create box plot
    fig = px.box(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        points=points,
        notched=notched,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        xaxis_title=x,
        yaxis_title=y,
        legend_title=color if color else None,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_distribution_chart(
    data: pd.DataFrame,
    column: str,
    title: str = None,
    color: str = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a distribution chart (histogram with KDE) using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        column (str): Column name for the distribution
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create figure
    fig = go.Figure()
    
    # Add histogram
    fig.add_trace(go.Histogram(
        x=data[column],
        histnorm='probability density',
        name='Histogram',
        marker_color='#4285F4',
        opacity=0.7
    ))
    
    # Add KDE
    try:
        from scipy import stats
        
        # Get column data
        x = data[column].dropna()
        
        # Create KDE
        kde_x = np.linspace(x.min(), x.max(), 1000)
        kde = stats.gaussian_kde(x)
        kde_y = kde(kde_x)
        
        # Add KDE trace
        fig.add_trace(go.Scatter(
            x=kde_x,
            y=kde_y,
            mode='lines',
            name='KDE',
            line=dict(color='#EA4335', width=2)
        ))
    except:
        # Skip KDE if scipy is not available
        pass
    
    # Update layout
    fig.update_layout(
        title=title,
        title_x=0.5,
        xaxis_title=column,
        yaxis_title='Density',
        height=height,
        template=template,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_correlation_matrix(
    data: pd.DataFrame,
    title: str = None,
    colorscale: str = 'RdBu_r',
    zmin: float = -1,
    zmax: float = 1,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a correlation matrix using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the correlation matrix
        title (str, optional): Chart title
        colorscale (str, optional): Colorscale for the heatmap
        zmin (float, optional): Minimum value for the color scale
        zmax (float, optional): Maximum value for the color scale
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create correlation matrix
    corr_matrix = data.corr()
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale=colorscale,
        zmin=zmin,
        zmax=zmax,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        hovertemplate='%{x} - %{y}<br>Correlation: %{z:.2f}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        title_x=0.5,
        height=height,
        template=template,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_area_chart(
    data: pd.DataFrame,
    x: str,
    y: Union[str, List[str]],
    title: str = None,
    color: str = None,
    groupnorm: str = None,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create an area chart using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        x (str): Column name for x-axis
        y (Union[str, List[str]]): Column name(s) for y-axis
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        groupnorm (str, optional): Group normalization ('fraction', 'percent')
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create area chart
    fig = px.area(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        groupnorm=groupnorm,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        xaxis_title=x,
        yaxis_title=y if isinstance(y, str) else None,
        legend_title=color if color else None,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_funnel_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = None,
    color: str = None,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a funnel chart using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        x (str): Column name for x-axis (values)
        y (str): Column name for y-axis (stages)
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create funnel chart
    fig = px.funnel(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_radar_chart(
    data: pd.DataFrame,
    r: Union[str, List[str]],
    theta: str,
    title: str = None,
    color: str = None,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a radar chart using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        r (Union[str, List[str]]): Column name(s) for radius values
        theta (str): Column name for angle values
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create radar chart
    fig = px.line_polar(
        data,
        r=r,
        theta=theta,
        line_close=True,
        color=color,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, data[r].max() * 1.1] if isinstance(r, str) else None
            )
        )
    )
    
    return fig

def create_treemap(
    data: pd.DataFrame,
    path: List[str],
    values: str,
    title: str = None,
    color: str = None,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a treemap using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        path (List[str]): List of column names for hierarchical path
        values (str): Column name for values
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create treemap
    fig = px.treemap(
        data,
        path=path,
        values=values,
        title=title,
        color=color,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_sunburst(
    data: pd.DataFrame,
    path: List[str],
    values: str,
    title: str = None,
    color: str = None,
    color_discrete_map: Dict = None,
    height: int = None,
    template: str = 'plotly_white'
) -> go.Figure:
    """
    Create a sunburst chart using Plotly.
    
    Args:
        data (pd.DataFrame): The DataFrame containing the data
        path (List[str]): List of column names for hierarchical path
        values (str): Column name for values
        title (str, optional): Chart title
        color (str, optional): Column name for color encoding
        color_discrete_map (Dict, optional): Mapping of categories to colors
        height (int, optional): Chart height in pixels
        template (str, optional): Plotly template
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create sunburst
    fig = px.sunburst(
        data,
        path=path,
        values=values,
        title=title,
        color=color,
        color_discrete_map=color_discrete_map,
        height=height,
        template=template
    )
    
    # Update layout
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig
