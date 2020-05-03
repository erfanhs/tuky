function setTooltip(el) {
    $(el).attr('data-original-title', 'Copied')
    .tooltip('show');
}
function hideTooltip(el) {
    setTimeout(function() {
        $(el).attr('data-original-title', 'Copy')
        .tooltip('hide');
    }, 700);
}
function copy(text, el) {
    setTooltip(el);
    textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    hideTooltip(el);
}
function sliceText(text, end=140) {
    if (text.length <= end) return text
    return text.slice(0, end) + '...'
}