def get_graph():
    """
    creates a graph encodes it in utf-8
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    #at the start of the buffer
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
    """
    pass

def get_plot(sizes, labels):
    """
    # where I am going to create the eleements
    plt.switch_backend("AGG")
    # labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    # sizes = [15, 30, 45, 10]
    # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots(figsize=(2,2))
    plt.title("Totalidad Personas")
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal') 
    graph = get_graph()
    return graph
    """
    pass



def get_plot_bar(x, y):
    """
    # where I am going to create the eleements
    plt.switch_backend("AGG")   
    plt.figure(figsize=(4,3))
    plt.title("Historico")
    plt.bar(x, y)
    plt.xlabel("Periodos")
    plt.ylabel("Numero personas")
    plt.tight_layout()
    graph = get_graph()
    return graph
    """
    pass