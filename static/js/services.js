// api calls and responses
async function login() {
    let myForm = document.getElementById('login-form');
    let formData = new FormData(myForm);
    try {
        let res = await fetch('/login', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "username": formData.get("username"),
                "password": formData.get("password")
            })
        });
        let response = await res.json()
        if (response.success) window.location.href = '/dashboard'
        else alert(response.message)
    }
    catch (err) {
        console.log(err)
    }
}

async function upsert_tracker(tracker_id=null) {
    let myForm = document.getElementById('tracker-form');
    let formData = new FormData(myForm);
    try {
        let url = (!tracker_id) ? "/create_tracker" : `/edit_tracker?tracker_id=${tracker_id}`
        let res = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "name": formData.get("name"),
                "description": formData.get("description"),
                "tracker_type": formData.get("tracker_type"),
                "settings": formData.get("settings")
            })
        })
        let response = await res.json()
        if (response.success) window.location.href = '/dashboard'
        else alert(response.message)
    }
    catch (err) {
        console.log(err)
    }
}

async function upsert_log(tracker_id, log_id=null) {
    let myForm = document.getElementById('log-form');
    let formData = new FormData(myForm);
    try {
        let url = (!log_id) ? `/create_log?tracker_id=${tracker_id}` : `/edit_log?tracker_id=${tracker_id}&log_id=${log_id}`
        let res = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "timestamp": convert_date_to_timestamp(formData.get("timestamp")),
                "value": formData.get("value"),
                "note": formData.get("note")
            })
        })
        let response = await res.json()
        if (response.success) window.location.href = `/tracker_info?tracker_id=${tracker_id}`
        else alert(response.message)
    }
    catch (err) {
        console.log(err)
    }
}

function convert_date_to_timestamp(timestamp) {
    let date = new Date(timestamp)
    return parseInt(date.getTime())
}