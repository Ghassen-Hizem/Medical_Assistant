export default function ChatSection() {
    return(
        <>

        <div className="ml-8 mt-16 mr-8 h-5/6 border-2 shadow-[5px_5px_0px_0px_rgba(0,0,0)] border-solid border-black">
          <div className=" h-full flex flex-col justify-end">
    
           <form>
            <input className=" bg-white w-11/12 h-16 border-2 border-black border-solid" type="text"/>
            <button type="submit" className="w-1/12 border-2 border-black h-16">Send</button>
           </form>
           </div>
        </div>
        </>
    )
}