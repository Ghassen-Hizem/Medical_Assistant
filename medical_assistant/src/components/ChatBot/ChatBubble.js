export default function ChatBubble({message}) {

    return(

        <>
        <div className="flex flex-row mt-8 mb-8">
            <div className=" h-fit ">
            <img className="object-cover w-10 h-10 rounded-full" src="https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80" alt="avatar"/>
            </div>
            <div className="break-all bg-white ml-4 text-black p-2 w-10/12 h-fit rounded-lg">
                    {message}
                </div>
                </div>
        </>
    )


}