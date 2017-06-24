function show_full(element, review_id) {
    var review = document.querySelector("[data-reviewpk='"+review_id+"']");
    $(review.getElementsByClassName('short')[0]).toggle();
    $(review.getElementsByClassName('full')[0]).toggle();
}