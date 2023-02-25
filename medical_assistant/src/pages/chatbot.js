import ChatSection from "@/components/ChatSection";
import NavBarChat from "@/components/NavBarChat";
import SideBar from "@/components/SideBar";

export default function ChatBot() {

    return(
        <>
        <div className="w-full h-screen ">
            <div className="flex flex-row">
                
                <SideBar></SideBar>
                <div className="w-full h-screen">
                <NavBarChat></NavBarChat>
                <ChatSection></ChatSection>
                </div>
                </div>
        </div>
        </>
    )

}