import json

import matplotlib.pyplot as plt


def inspect_dataframe(dataframe):

    dataframe_info = {
        "columns": dataframe.columns.tolist(),
        "data_types": dataframe.dtypes.astype(str).to_dict(),
        "row_count": len(dataframe),
        "sample_data": dataframe.head(5).to_dict(orient="records")
    }

    return dataframe_info

def parse_chart_recommendation(recommendation):
    try:
        chart_config = json.loads(recommendation)

        return {
            'success' : True,
            'config': chart_config,
            'error': None
        }
    except json.JSONDecodeError as error:
        return {
            'success': False,
            'config' : None,
            'error' : str(error)
        }

def validate_chart_config(chart_config,dataframe):
    allowed_chart_types={"bar","line","scatter","pie"}
    chart_type = chart_config.get("chart_type")
    x_column=chart_config.get("x_column")
    y_column=chart_config.get('y_column')

    if chart_type not in allowed_chart_types:
        return {
            "valid":False,
            "error":f"Unsupported chart type:{chart_type}"
        }

    if x_column not in dataframe.columns:
        return {
            "valid": False,
            "error": f"Column not found: {x_column}"
        }

    if y_column not in dataframe.columns:
        return {
            "valid": False,
            "error": f"Column not found: {y_column}"
        }

    return {
        "valid": True,
        "error": None
    }

def generate_chart(dataframe,chart_config,output_path="output_chart.png"):
    chart_type = chart_config['chart_type']
    x_column= chart_config['x_column']
    y_column = chart_config['y_column']
    title = chart_config['title']

    if chart_type == 'bar':
        plt.figure(figsize=(10,6))
        plt.bar(
            dataframe[x_column],
            dataframe[y_column]
        )
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(title)

        plt.xticks(rotation=45,ha='right')
        plt.tight_layout()

    elif chart_type=='line':
        plt.figure(figsize=(10,6))
        plt.plot(
            dataframe[x_column],
            dataframe[y_column]
        )
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(title)

        plt.xticks(rotation=45,ha="right")
        plt.tight_layout()

    elif chart_type == "scatter":
    
            plt.figure(figsize=(10, 6))
    
            plt.scatter(
                dataframe[x_column],
                dataframe[y_column]
            )
    
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(title)
    
            plt.tight_layout()
    
    elif chart_type == "pie":

        plt.figure(figsize=(8, 8))

        plt.pie(
            dataframe[y_column],
            labels=dataframe[x_column],
            autopct="%1.1f%%"
        )

        plt.title(title)
        plt.tight_layout()

    plt.savefig(output_path)
    plt.close()

    return output_path