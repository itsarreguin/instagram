// <span class="text-gray">{{ notification.created|timesince }} ago</span>

function notificationCard(notification) {
  return /*html*/`
    <a
      id="notification-${notification.slug}"
      class="card-notification flex flex-align-center flex-justify-between ${notification.is_read ? "" : "notification-not-read"}"
      href="/notifications/${notification.slug}/${notification.object_slug}/"
    >
      <div class="flex">
        <section class="notification-user">
          <span class="profile-default flex flex-align-center flex-justify-center">
            ${notification.sender.profile.picture ?
                /*html*/`<img src="${ notification.sender.profile.picture }" alt="Sender profile picture">`
              :
                /*html*/`
                <span class="profile-default flex flex-align-center flex-justify-center">
                  ${ String(notification.sender.first_name).slice(0,1) }${ String(notification.sender.last_name).slice(0,1) }
                </span>`
            }
          </span>
        </section>
        <section class="" style="margin-left: 15px;">
          <h4 class="mb-8">${ notification.sender.first_name } ${ notification.sender.last_name }</h4>
          <span style="font-size: 16px;">
            <span class="text-dark" style="margin-right: 10px;">
              ${notification.category === "follower" ? "Started following you" : ""}
              ${notification.category === "like" ? "Liked your post" : ""}
              ${notification.category === "comment" ? "Commented your post" : ""}
            </span>
          </span>
        </section>
      </div>
      <div>
        <form hx-delete="/notifications/${notification.pk}/" hx-target="closest #notification" hx-swap="outerHTML swap:0.2s" style="padding: 4px;">
          <button type="submit">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#C13434" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
          </button>
        </form>
      </div>
    </a>
  `;
}

function notificationsEventSource() {
  const protocol = window.location.protocol;
  const host = window.location.hostname;
  const port = window.location.port;
  const source = new EventSource(protocol + "//" + host + ":" + port + "/sse/notifications/");

  source.onopen = function(event) {
    console.log("Notifications Event connection accepted");
  }

  source.onmessage = function(event) {
    const notifications = JSON.parse(event.data);
    let list = document.getElementById("notifications");
    let counter = document.getElementById("notifications-counter");
    let notificationElement = ``;

    let unreadNotifications = notifications.filter((notification) => {
      return notifications.length ? notification.is_read === false : 0;
    });

    if (notifications.length > 0 && unreadNotifications.length > 0 && counter) {
      counter.style.display = "flex";
      counter.innerText = unreadNotifications.length;
    }

    notifications.map((notification) => {
      if (list) {
        notificationElement += notificationCard(notification);
        list.innerHTML = notificationElement;
      }
    });
  }

  source.onclose = function(event) {
    console.log("Notifications Event connection accepted");
  }
}

notificationsEventSource();