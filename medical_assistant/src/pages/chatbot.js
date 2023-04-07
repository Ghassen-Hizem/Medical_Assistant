import ChatSection from "@/components/ChatSection";
import NavBarChat from "@/components/NavBarChat";
import SideBar from "@/components/SideBar";

export default function ChatBot() {

    return(
        <>
        <div className=" flex flex-col h-screen">
         <div >
        <NavBarChat></NavBarChat>
        </div>
        <div className="grow flex flex-row custom-background gap-24">
        
        <SideBar></SideBar>
        <ChatSection></ChatSection>
        </div>
        </div>
        </>
    )

}