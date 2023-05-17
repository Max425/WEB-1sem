function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(".love-btn").on('click', function (ev) {
    const loveBtn = this; 

    const request = new Request(
        'http://127.0.0.1:8000/vote_up/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'object_id=' + $(this).data('id') + '&type=' + $(this).data('type'),
        }
    );

    fetch(request)
        .then(response_raw => response_raw.json())
        .then(response_json => {
            $(loveBtn).closest(".counter").find(".counter-input").val(response_json.new_like);
        });
});

$(".form-check-input").on('click', function (ev) {
    const checkInput = this;

    const request = new Request(
        'http://127.0.0.1:8000/is_correct/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'answer_id=' + $(this).data('id'),
        }
    );

    fetch(request)
        .then(response_raw => response_raw.json())
        .then(response_json => {
            $(checkInput).prop('checked', response_json.correct);
        });
});
