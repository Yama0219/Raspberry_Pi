from matplotlib import pyplot as plt
import japanize_matplotlib

def TablePlot_image(df,w,h,outputPath):
    fig, ax = plt.subplots(figsize=(w,h))
    ax.axis('off')
    ax.table(
        df.values,
        colLabels = df.columns,
        loc = 'center',
        bbox=[0,0,1,1]
    )
    plt.savefig(outputPath)

def TablePlot_html(df, outputpath):
    html = df.to_html()
    text_file = open(outputpath,"w")
    text_file.write(html)
    text_file.close()