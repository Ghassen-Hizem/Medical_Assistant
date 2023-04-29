import NextAuth from "next-auth"
import  CredentialsProvider  from "next-auth/providers/credentials"

const authOptions = {

  secret: "some secret",


    session: {
        strategy: 'jwt'
    },

  providers: [
    CredentialsProvider({


        type: 'credentials',
        credentials: {

        },

       async authorize(credentials, req) {
          const {email, password} = credentials;
          
          if (email!=="ghassen@gmailcom" && password !=="1234") {
            throw new Error("invalid credentials");
          }

          return {id:'1234' , name: 'ghassen hizem' , email: "ghassen@gmail.com"}
        }
    })
  ],
  pages: {
    signIn: '/auth/login'
  }

}

export default NextAuth(authOptions)