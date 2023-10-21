function senderCard(message) {
  return /*html*/ `
    <section class="flex flex-align-start flex-justify-end mb-10">
      <div class="text-14px" style="padding: 8px 10px; border-radius: 8px; border-top-right-radius: 0px; background: #3CA1FF; color: #FFFFFF;">
        ${ message.body }
      </div>
      <div class="card-user-picture ml-10">
        ${
          message.sender.profile.picture
          ? /*html*/`<img src="${ message.sender.profile.picture }" alt="${ message.sender.username }-profile-pic">`
          : /*html*/`
            <span class="profile-default flex flex-justify-center flex-align-center">
              ${ String(message.sender.first_name).slice(0,1) }${ String(message.sender.last_name).slice(0,1) }
            </span>
            `
        }
      </div>
    </section>
  `;
}

function receiverCard(message) {
  return /*html*/`
  <section class="flex flex-align-start flex-justify-start mb-10">
    <div class="card-user-picture mr-10">
      ${
        message.sender.profile.picture
        ? /*html*/`<img src="${ message.sender.profile.picture }" alt="${ message.sender.username }-profile-pic">`
        : /*html*/`
          <span class="profile-default flex flex-justify-center flex-align-center">
            ${ String(message.sender.first_name).slice(0,1) }${ String(message.sender.last_name).slice(0,1) }
          </span>
          `
      }
    </div>
    <div class="text-14px" style="padding: 8px 10px; border-radius: 8px; border-top-left-radius: 0px; background: #808CA4; color: #FFFFFF;">
      ${ message.body }
    </div>
  </section>
  `;
}

function messagesWebSocket() {
  const host = window.location.hostname;
  const port = window.location.port;
  const socket = new WebSocket("ws://" + host + ":" + port + "/ws/messages/" + inboxId + "/");

  let form = document.getElementById("message-form");
  let messagesList = document.getElementById("messages-list");
  let messageCard = ``

  socket.addEventListener("open", () => {
    console.log("WebSocket Connection accepted");
  })

  socket.addEventListener("message", (event) => {
    let data = JSON.parse(event.data);
    let sender = data.message.sender;

    if (sender.username == currentUser) {
      messageCard += senderCard(data.message);
      messagesList.innerHTML += messageCard;
    } else {
      messageCard += receiverCard(data.message)
      messagesList.innerHTML += messageCard;
    }
  });

  socket.addEventListener("close", (event) => {
    console.error("Websocket connection failed");
    setTimeout(() => {
      console.log("Reconnection ...");
      messagesWebSocket();
    }, 2000)
  });

  socket.addEventListener("error", (err) => {
    console.error("WebSocket encountered an error: " + err.message);
    console.log("Socket closing");
    socket.close();
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    let input = document.getElementById("message");
    socket.send(JSON.stringify({ "message": input.value, "receiver": receiverUsername }));
    input.value = "";
  })
}

messagesWebSocket();