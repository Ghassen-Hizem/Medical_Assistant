import ChatSection from "@/components/ChatSection";
import NavBarChat from "@/components/NavBarChat";
import SideBar from "@/components/SideBar";
import  {useSession} from "next-auth/react";
import { useEffect } from "react";
import { useRouter } from "next/router";

export default function ChatBot() {

 const router = useRouter();
    const {status, data} = useSession();

    useEffect(() => {
        if(status ==="unauthenticated") {
            router.push("/auth/login");
        }

        if(status === "authenticated") {
            console.log('welcome')
        }
    }, [status])

    return(
        <>
          <div className=" flex flex-col h-screen">
                <div>
               <NavBarChat></NavBarChat>
               </div>
               <div className="grow flex flex-row custom-background ">
               
               <SideBar></SideBar>
               <ChatSection></ChatSection>
               </div>
               </div>
        </>
    )

}

