import ChatSection from "@/components/ChatSection";
import NavBarChat from "@/components/NavBarChat";
import SideBar from "@/components/SideBar";

export default function ChatBot() {

    return(
        <>
        <NavBarChat></NavBarChat>
        <div className="flex flex-row custom-background gap-24">
        <SideBar></SideBar>
        <ChatSection></ChatSection>
        </div>
        </>
    )

}