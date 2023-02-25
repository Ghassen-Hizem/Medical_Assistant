import ChatBubble from "./ChatBot/ChatBubble";

export default function ChatSection() {
    return(
        <>

        <div className="ml-8 mt-16 mr-8 h-5/6 border-2 shadow-[5px_5px_0px_0px_rgba(0,0,0)] border-solid border-black">
        <div className="flex flex-col justify-end">
          <ChatBubble></ChatBubble>
           <form>
            <div className="flex ">
            <textarea className="bg-white w-11/12 border-2 border-black border-solid" type="text"/>
            <button type="submit" className="w-1/12 border-2 border-black ">Send</button>
            </div>
           </form>
           
        </div>
        </div>
        </>
    )
}