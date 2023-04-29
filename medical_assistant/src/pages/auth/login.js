import { signIn  } from "next-auth/react";
import Link from "next/link";

import { useRouter } from "next/router";
import { useState } from "react";


export default function Login() {
  const router = useRouter();

  const [credentials, Setcredentials] = useState({
    email: '',
    password: '',
  });

  async function handleSubmit() {
    const res = await signIn("credentials", {
      email: credentials.email,
      password: credentials.password,
      redirect: false,
    })

    if(res.ok == true) {
      router.push("/chatbot");
    }
    else{
      alert("wrong credentials");
    }

 
  }


  return (
    <>
      <div className="bg-gray-100 flex h-screen flex-col justify-center">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <img style={{ height: '200px' }} className="mx-auto w-auto" src="/violet.png" alt="Your Company" />
          <h2 className=" text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" onSubmit={(e) => {
            e.preventDefault();
            handleSubmit();
          }} >
            <div>
              <label for="email" className="block text-sm font-medium leading-6 text-gray-900">Email address</label>
              <div className="mt-2">
                <input onChange={(e) => {
                  Setcredentials({
                    ...credentials,
                    email: e.target.value
                  })
                }} id="email" placeholder="   enter email here" name="email" type="email" autocomplete="email" required className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label for="password" className="block text-sm font-medium leading-6 text-gray-900">Password</label>
                <div className="text-sm">
                  <a href="#" className="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
                </div>
              </div>
              <div className="mt-2">
                <input onChange={(e) => {
                  Setcredentials({
                    ...credentials,
                    password: e.target.value
                  })
                }} id="password" placeholder="   *******" name="password" type="password" autocomplete="current-password" required className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
              </div>
            </div>

            <div>
              <button type="submit" className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Sign in</button>
            </div>
            <div>

            </div>

          </form>

          <p className="mt-10 text-center text-sm text-gray-500">
            Not a member?
            <Link href="/auth/register" className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">  Create Account</Link>
          </p>
        </div>
      </div>
    </>
  )
}