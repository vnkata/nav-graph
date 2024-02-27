/*
 * Created by nphau on 9/19/22, 9:31 PM
 * Copyright (c) 2022 . All rights reserved.
 * Last modified 9/19/22, 9:31 PM
 */

const onButtonExtendedGraphListener = () => {
    let btnExtendedGraph = document.getElementById('button-graph-extend')
    if (btnExtendedGraph != null) {
        btnExtendedGraph.onclick = (event) => {
            let sideBar = document.getElementById('sidebar-card')
            let icon = document.getElementById('button-graph-extend-icon')
            //
            if (sideBar.style.display === 'none') {
                sideBar.style.display = ''
                icon.className = "bi bi-chevron-double-right";
            } else {
                sideBar.style.display = 'none'
                icon.className = "bi bi-chevron-double-left";
            }
        };
    }
}
const onRunToThisPlayClickListener = () => {

}
//
// const onScreenshotClickListener = () => {
//     let screenshotElement = document.getElementById('id-screenshot')
//     if (screenshotElement != null) {
//         screenshotElement.onclick = (event) => {
//             let imageTag = screenshotElement.getElementsByTagName('img')[0];
//             let image = new Image();
//             image.src = imageTag.src;
//             let w = window.open("");
//             w.document.title = "Viewer"
//             w.document.write('<title>Viewer</title>');
//             w.document.write('<link rel="icon" href="https://katalon.com/hubfs/katalon_small_transparent.svg">');
//             w.document.write(image.outerHTML);
//         };
//     }
// }
document.addEventListener('readystatechange', event => {
    switch (document.readyState) {
        case "loading":
            console.log("document.readyState: ", document.readyState,
                `- The document is still loading.`
            );
            break;
        case "interactive":
            console.log("document.readyState: ", document.readyState,
                `- The document has finished loading DOM. `,
                `- "DOMContentLoaded" event`
            );
            break;
        case "complete":
            setTimeout(function () {
                onButtonExtendedGraphListener()
                onRunToThisPlayClickListener()
                // onScreenshotClickListener()
            }, 3000);
            break;
    }
});