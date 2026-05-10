
function matrixRain(){

const chars='01ABCDEF#@$%';
let txt='';

for(let i=0;i<6000;i++){

txt += chars[Math.floor(Math.random()*chars.length)];

if(i % 120 === 0) txt += '\n';

}

document.getElementById('matrix').innerText = txt;

}

setInterval(matrixRain,500);

const terminal = document.getElementById('terminal');
const input = document.getElementById('commandInput');

if(input){

const commands = {
help:'help scan hack decrypt trace matrix ddos proxy firewall connect dump',
scan:'[ NETWORK SCAN COMPLETE ]',
hack:'[ ACCESS GRANTED ]',
decrypt:'[ PASSWORD DECRYPTED ]',
trace:'[ TARGET TRACED ]',
matrix:'0101010101010101',
ddos:'[ DDOS ACTIVE ]',
proxy:'[ PROXY ENABLED ]',
firewall:'[ FIREWALL DISABLED ]',
connect:'[ REMOTE SERVER CONNECTED ]',
dump:'[ DATABASE DOWNLOADED ]'
};

input.addEventListener('keypress', e=>{

if(e.key==='Enter'){

const cmd = input.value.toLowerCase();

const line = document.createElement('div');
line.innerHTML = '>> ' + cmd;

terminal.appendChild(line);

const response = document.createElement('div');
response.innerHTML = commands[cmd] || 'UNKNOWN COMMAND';

terminal.appendChild(response);

terminal.scrollTop = terminal.scrollHeight;

input.value='';

}

});

}

async function askAI(){

const text = document.getElementById('aiInput').value;

const res = await fetch('/chatbot?q=' + text);

const data = await res.json();

document.getElementById('aiResponse').innerHTML = data.response;

}
