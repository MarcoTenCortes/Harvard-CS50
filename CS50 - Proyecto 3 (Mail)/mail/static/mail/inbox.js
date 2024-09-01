
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
  // Handling the email sending process
  document.querySelector('form').onsubmit = () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    document.querySelector('#compose-body').setAttribute('style', 'height: auto !important;');
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
    });
    return false;
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Load the mailbox emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      
      const email_div = document.createElement('div');
      email_div.className = 'email-item';
      if (email.read) {
        email_div.style.backgroundColor = 'gray';
        email_div.onmouseover = function() {
          email_div.style.backgroundColor = '#b3b3b3'; // Color de hover para emails leídos
        };
        email_div.onmouseout = function() {
          email_div.style.backgroundColor = 'gray';
        };
      } else {
        email_div.style.backgroundColor = 'white';
        email_div.onmouseover = function() {
          email_div.style.backgroundColor = '#f0f0f0'; // Color de hover para emails no leídos
        };
        email_div.onmouseout = function() {
          email_div.style.backgroundColor = 'white';
        };
      }
      console.log(email.read)
      // Check if the mailbox is 'sent' to show the recipient instead of the sender
      if (mailbox === 'sent') {
        email_div.innerHTML = `
          <span class="email-recipient">${email.recipients.join(', ')}</span>
          <span class="email-subject">${email.subject}</span>
          <span class="email-timestamp">${email.timestamp}</span>`;
      } else {
        email_div.innerHTML = `
          <span class="email-sender">${email.sender}</span>
          <span class="email-subject">${email.subject}</span>
          <span class="email-timestamp">${email.timestamp}</span>`;
      }

      email_div.addEventListener('click', () => load_email(email.id));
      document.querySelector('#emails-view').append(email_div);
    });
  });
}

function load_email(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#emails-view').innerHTML = `
      <ul>
        <li><strong>From:</strong> ${email.sender}</li>
        <li><strong>To:</strong> ${email.recipients}</li>
        <li><strong>Subject:</strong> ${email.subject}</li>
        <li><strong>Timestamp:</strong> ${email.timestamp}</li>
        <li>${email.body}</li>
      </ul>
      <button id="reply" class="btn_mail">Reply</button>`;
    
    // Archive/Unarchive logic
    const btn_arch = document.createElement('button');
    btn_arch.innerHTML = email.archived ? "Unarchive" : "Archive";
    btn_arch.className = "btn_mail"
    btn_arch.addEventListener('click', function() {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then(() => {load_mailbox('inbox')})
    });
    document.querySelector('#emails-view').append(btn_arch);

    // Event listener for reply button
    document.querySelector('#reply').addEventListener('click', () => {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      document.querySelector('#compose-body').value = `\n\n---\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;    });
  });
}
