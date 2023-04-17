
import {  useState } from "react";
import ChatBubble from "./ChatBot/ChatBubble";
import useWebSocket from 'react-use-websocket';

let nextId = 0;

export default function ChatSection() {

  const  [Message , SetMessage] = useState('');

  const  [MessageArray,SetmessageArray] = useState([]);

  const {
    sendMessage,

  } = useWebSocket('ws://localhost:8000/api', {
    onOpen: () => console.log('opened'),
    onMessage: (event) => {
            SetmessageArray([
                ...MessageArray,
                { id: nextId++, message:event.data }
              ])
    },

  });   



    function handleChange(e){
        SetMessage(e.target.value); 
    }

    const listItems = MessageArray.map(bubble =>
        <li key={bubble.id} >
            <ChatBubble message={bubble.message} ></ChatBubble>
        </li>
        )

    return(
        <>
        <div className="chat-background w-full text-white  flex flex-col justify-between">
        <div className="ml-8">
<ul>
    {listItems}
</ul>
        </div>
        <form onSubmit={(e) => {
            e.preventDefault();
            sendMessage(Message)
             SetmessageArray([
            ...MessageArray,
            { id: nextId++, message:Message }
          ])
          SetMessage('');
            }}>
        <div className="ml-8 mb-8 flex flex-row " >
<input value={Message} onChange={handleChange} className="w-10/12 h-12 rounded-lg text-black pl-4 break-all" placeholder="Type Here !" type="text">

</input>
<button className="ml-4 button-color w-32 rounded-lg text-lg font-bold">Send</button>
        </div>
        </form>
        </div>
        </>
    )
}