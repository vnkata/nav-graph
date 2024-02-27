// Dash JS
const fill_default = (element) => {
    let polygon = element.children[1]
    polygon.setAttribute("fill", "white")
    polygon.setAttribute("stroke", "grey")
    let text = element.children[2]
    if (text != null) {
        text.setAttribute("fill", "black")
    }
}
const fill_visited = (element) => {
    let polygon = element.children[1]
    polygon.setAttribute("fill", "#00A86B")
    polygon.setAttribute("stroke", "#00A86B")
    let text = element.children[2]
    text.setAttribute("fill", "white")
    let lastLetter = text.textContent.charAt(text.textContent.length - 1)
    if (lastLetter !== "✔") {
        text.textContent = text.textContent + "✔"
    }
}
const fill_edge = (element) => {
    let path = element.children[1]
    path.setAttribute("stroke", "rgb(0, 100, 0)")
    let polygon = element.children[2]
    polygon.setAttribute("fill", "rgb(0, 100, 0)")
    polygon.setAttribute("stroke", "rgb(0, 100, 0)")
}
const fill_node_with_symbol = (element, success = false) => {
    let polygon = element.children[1]
    polygon.setAttribute("fill", "#00A86B")
    polygon.setAttribute("stroke", "#00A86B")
    let text = element.children[2]
    text.setAttribute("fill", "white")

    if (element.children[element.children.length - 1].getAttribute("is_symbol") != null)
        return

    let symbol_label = text.cloneNode(true);
    if (polygon.tagName === 'polygon') {
        offset = parseFloat(polygon.getAttribute("points").split(" ")[0]);
        xlocation = offset + 5;
    } else {
        //ellipse
        offset = parseFloat(polygon.getAttribute("cx"));
        const bbox = element.getBBox();
        const {
            width,
            height
        } = bbox;
        console.log(width, height)
        xlocation = offset + width / 2 + 10;
    }
    symbol_label.setAttribute("x", xlocation)
    symbol_label.setAttribute("is_symbol", true)
    if (success === true) {
        symbol_label.setAttribute("fill", "#00A86B")
        symbol_label.innerHTML = "✔"
    } else {
        symbol_label.setAttribute("fill", "#960018")
        symbol_label.innerHTML = "✘"
    }
    element.appendChild(symbol_label)

}
const fill_node = (element) => {
    let polygon = element.children[1]
    polygon.setAttribute("fill", "#2A52BE")
    polygon.setAttribute("stroke", "#2A52BE")
    let text = element.children[2]
    if (text != null) {
        text.setAttribute("fill", "white")
    }
}
const fill_init_node = (element) => {
    let polygon = element.children[1]
    if (polygon.getAttribute('fill') === '#2A52BE')
        polygon.setAttribute("fill", "white")
    polygon.setAttribute("stroke", "#00A86B")
    let text = element.children[2]
    if (polygon.getAttribute('fill') === 'white')
        text.setAttribute("fill", "black")
}
const socket_highlight_path = (new_path = []) => {
    let graph = document.getElementById("graph0")
    if (graph != null && new_path != null) {
        let edges = []
        for (let i = 0; i < new_path.length - 1; i++) {
            edges.push(new_path[i] + "->" + new_path[i + 1])
            edges = [...new Set(edges)]
        }
        let children = graph.children
        for (let i = 0; i < children.length; i++) {
            let element = children[i]
            let title_tag = element.firstElementChild
            if (title_tag != null) {
                let id = title_tag.textContent
                if (new_path.includes(id)) {
                    fill_init_node(element)
                }
                if (edges.includes(id)) {
                    fill_edge(element)
                }
            }
        }
    }
}

const get_element_by_node = (selected_node) => {
    let graph = document.getElementById("graph0")
    if (graph != null) {
        let children = graph.children
        for (let i = 0; i < children.length; i++) {
            let element = children[i]
            let title_tag = element.firstElementChild
            if (title_tag != null) {
                let id = title_tag.textContent
                if (id === selected_node) {
                    return element
                }
            }
        }
    }
    return null
}
const socket_play = (selected_node) => {
    let graph = document.getElementById("graph0")
    if (graph != null) {
        let children = graph.children
        for (let i = 0; i < children.length; i++) {
            let element = children[i]
            let title_tag = element.firstElementChild
            if (title_tag != null) {
                let id = title_tag.textContent
                if (id === selected_node) {
                    selected_nodes.push(id)
                    selected_nodes = [...new Set(selected_nodes)]
                    // fill_visited(element)
                }
            }
        }
    }
}
const SOCKET_TYPE_INIT = "INIT"
const SOCKET_TYPE_UPDATE_CURRENT_POSITION = "UPDATE_CURRENT_POSITION"
let selected_nodes = []
let selected_path = []
let previous_clicked_element = null

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        // When user click on graph
        onUserSelectNode: function (selected_node) {
            let graph = document.getElementById("graph0")
            if (graph != null) {
                let children = graph.children
                if (previous_clicked_element != null) {
                    fill_default(previous_clicked_element)
                }
                for (let i = 0; i < children.length; i++) {
                    let element = children[i]
                    let title_tag = element.firstElementChild
                    if (title_tag != null) {
                        let id = title_tag.textContent
                        if (id === selected_node) {
                            fill_node(element)
                            previous_clicked_element = element
                            return selected_node
                        }
                    }
                }
            }
            // return ""
        },
        // Socket Listener
        onSocketListener: function (msg) {
            if (!msg) return {};
            let msg_data = JSON.parse(msg.data)
            console.log("** received message: ", msg_data)
            const data = JSON.parse(msg_data)
            let new_path = []
            let type = data['type']
            if (type === SOCKET_TYPE_INIT) {
                new_path = data['value']
                // Combine
                selected_path = selected_path.concat(new_path)
                selected_path = [...new Set(selected_path)]
                socket_highlight_path(selected_path)
                return null
            } else if (type === SOCKET_TYPE_UPDATE_CURRENT_POSITION) {
                let node = data['node']
                let status = data['status']
                socket_play(node)
                let element = get_element_by_node(node)
                fill_node(element)
                setTimeout(function () {
                    fill_node_with_symbol(element, status)
                }, 1000);
                return node
            }
        },
        // Toggle extending graph
        showPlayToHereButton: function (selected) {
            console.log("showPlayToHereButton")
            console.log("clicks: " + selected)
            //return {"float": "right"}
            // if (style != null) {
            //     if (style['display'] == null) {
            //         console.log("style: " + style['display'])
            //         return [{}, "bi bi-chevron-double-right"]
            //     } else {
            //         return [{"display": "none"}, "bi bi-chevron-double-left"]
            //     }
            // } else {
            //     window.dash_clientside.no_update()
            // }
        }
    }
});
