import React, { useState, useRef } from "react";
import { useSearchParams } from "react-router-dom";
import axios from "axios";
import { authApi } from "../../api";


type FormType = "login" | "signup" | "forgot-password";
type customAuthMessageType = {
  type: "success" | "error" | "info";
  content: string;
};

const LoginForm: React.FC = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token')

  console.log("Current URL:", window.location.href);  // See the full URL
  console.log("Search params:", searchParams);        // See what searchParams contains
  console.log("Token value:", token);

  const [formType, setFormType] = useState<FormType>("login");
  const [customAuthMessages, setCustomAuthMessages] = useState<
    customAuthMessageType[]
  >([]);
  const authForm = useRef<HTMLFormElement>(null);

  // Function to check if all required fields are filled
  const checkRequiredFields = (
    formData: FormData,
    ...requiredFields: string[]
  ) =>
    requiredFields
      .map((x) => formData.get(x)?.toString().trim())
      .every(Boolean);


  // Function to handle form submission (**Example**)
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);

      /* Handle form submission (Forgot Password) */

      // Check if all required fields are filled
      if (!checkRequiredFields(formData, "new-password", "repeat-new-password")) {
        alert("Please fill all the required fields!");
        return;
      }


      const newPassword = formData.get('new-password')?.toString().trim()
      const repeatNewPassword = formData.get('repeat-new-password')?.toString().trim()

      // check if passwords match

      if (newPassword !== repeatNewPassword) {
        alert("Passwords don't match!");
        return;
      }

      try {
        if (!token) {
          console.log("TOKENNOTEXIST Your recovery link's got expired or it's missing. Please generate a new one through a Forgot password form")
          alert("Your recovery link's got expired or it's missing. Please generate a new one through a Forgot password form");
          return;
        }

        const response = await authApi.post('auth/postprocess-pswd-recovery', {
          token: token,
          new_password: newPassword
        });

        // If successful, show success message
          setCustomAuthMessages(() => [{
          type: "success",
          content: "Your password has been successfully updated! You can now try log in via login page"
          }]);

          } catch (error: any) {
          if (error.response) {
            switch (error.response.status) {
              case 400:
                console.log('Email is already taken!', error);
                alert('Account already exists with a such email! Please try another one, or recover your account via "Forgot password"');
                break;
              case 401:
                console.log('Wrong password or email', error);
                alert('Wrong password or email');
                break;
              case 404:
                console.log('Endpoint not found');
                alert("Endpoint not found");
                break;
              case 422:
                console.log("TOKENEXIST Your recovery link's got expired or it's missing. Please generate a new one through a Forgot password form");
                alert("Your recovery link's got expired or it's missing. Please generate a new one through a Forgot password form");
                break;
              case 500:
                console.log('Server error please try again later');
                alert("Server error, please try again later");
                break;
              default:
                console.log(`Unknown error: ${error.response.detail}`);
                alert("Unknown error, please try again later");
                break;
            }
          } else if (error.request) {
            alert('The server is unavailable, please check your internet connection or try again later');
          } else {
            alert('Unexpected error occured, please try again later');
          }
        }

      authForm.current?.reset();

      return;
      }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-[#3c6ff5] to-[#4c0bf4] px-4 py-2 md:px-0 md:py-0">
      <div className="rounded-xl bg-white px-10 py-8 shadow-lg md:w-96 md:rounded-[3rem] md:px-14 md:py-12 lg:w-[33.25rem]">
        <h2 className="mb-6 text-center text-xl font-bold">
          Please provide your new password to set up
        </h2>
        {!customAuthMessages.length ? (
          <>
            <form ref={authForm} onSubmit={handleSubmit}>
              <div className="mb-4">
                <label
                    className="block text-sm font-bold text-gray-700"
                    htmlFor="newPassword"
                >
                  New Password
                </label>
                <input
                    type="password"
                    id="newPassword"
                    name="new-password"
                    placeholder="Enter your new password"
                    className="mt-1 w-full border-2 border-gray-300 border-opacity-40 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    pattern="^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$"
                    title="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter and one digit"
                    min={8}
                    required={true}
                />
              </div>

              <div className="mb-4">
                <label
                    className="block text-sm font-bold text-gray-700"
                    htmlFor="repeatNewPassword"
                >
                  Repeat New Password
                </label>
                <input
                    type="password"
                    id="repeatNewPassword"
                    name="repeat-new-password"
                    placeholder="Repeat your new password"
                    className="mt-1 w-full border-2 border-gray-300 border-opacity-40 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    pattern="^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$"
                    title="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter and one digit"
                    min={8}
                    required={true}
                />
              </div>
              <div className="mb-4 text-center">
                <button
                    type="submit"
                    className="my-2 min-w-[15ch] rounded-3xl bg-black px-5 py-3 text-white transition-colors hover:bg-gray-800"
                >
                  Submit
                </button>
              </div>
            </form>
          </>
        ) : (
            <div className="mb-4 text-center text-sm font-semibold">
              {customAuthMessages.map((message, index) => (
                  <p
                      key={index}
                      className={`mb-2 ${message.type === "success" ? "text-green-600" : message.type === "error" ? "text-red-600" : "text-gray-600"}`}
                  >
                    {message.content}
                  </p>
              ))}
            </div>
        )}
      </div>
    </div>
  );
};

export default LoginForm;
