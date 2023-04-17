// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
let response = ''; 

export default function handler(req, res) {
    if(req.method =="POST") {
      response = req.body;
      console.log("i got it ")
      console.log(response)
    }
    res.send("hello")
}
