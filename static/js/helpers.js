let choices_ele = document.getElementById("choices_grp");
let tracker_type_ele = document.getElementById("tracker_type");
let timestamp_hidden_ele = document.getElementById("timestamp_val");
let timestamp_ele = document.getElementById("timestamp");

if (tracker_type_ele && tracker_type_ele.value === 'choices') choices_ele.classList.remove('d-none');
if (timestamp_hidden_ele && timestamp_hidden_ele.value) timestamp_ele.value = get_date_from_timestamp(timestamp_hidden_ele.value)
if (timestamp_hidden_ele && timestamp_hidden_ele.value) console.log(get_date_from_timestamp(timestamp))
else if (timestamp_ele) timestamp_ele.value = current_time()

function add_choices() {
    if (tracker_type_ele.value === 'choices') {
        choices_ele.classList.remove('d-none')
    }
    else {
        choices_ele.classList.add('d-none')
    }
}

function current_time() {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    let some = now.toISOString().slice(0, 16);
    return some
}

function get_date_from_timestamp(timestamp) {
    const date = new Date(parseInt(timestamp));
    date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
    let some = date.toISOString().slice(0, 16);
    return some
}

