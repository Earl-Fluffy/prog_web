function change_theme() {

    let bgColor = document.body.style.backgroundColor || window.getComputedStyle(document.body, null).backgroundColor;
    bgColor = (bgColor == "rgb(0, 0, 0)") ? "#f3f3f3" : "#000000";
    document.body.style.backgroundColor = bgColor;

    let fgColor = document.body.style.color || window.getComputedStyle(document.body, null).color;
    fgColor = (fgColor == "rgb(0, 0, 0)") ? "#f3f3f3" : "#000000";
    document.body.style.color = fgColor;
}

console.log("loaded");
