
"use client";
import { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { CardTitle, CardDescription, CardHeader, CardContent, CardFooter, Card } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { JSX, SVGProps } from "react";
import { QueryResultTable } from "@/components/QueryResultTable";
import { Data } from "@/types";
import { useRouter } from 'next/navigation';

export default function HomeComponent() {
    const [sqlQuery, setSqlQuery] = useState("");
    const [isValidQuery, setValidationResult] = useState(false);
    const [queryResult, setQueryResult] = useState<Data | null>(null);
    const router = useRouter();

    useEffect(() => {
        const username = localStorage.getItem("username");
        const host = localStorage.getItem("host");
        const password = localStorage.getItem("password");

        if (!username || !host || !password) {
           router.push("/landing")
        }
    }, []); 
    const backendUrl = "http://localhost:5000";

    const validateQuery = async () => {
        toast.promise(fetch(backendUrl + '/ValidateSQL', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: sqlQuery })
        }).then(response => response.json()), {
            success: "Valid SQL Query",
            error: "Invalid SQL Query",
            pending: "Validating SQL Query..."
        }).then(data => {
            if (data.success === true) {
                console.log(data.result);
                setValidationResult(true);
            } else {
                setValidationResult(false);
            }
        });
    };

    async function executeQuery() {
        toast.promise(fetch(backendUrl + '/ExecuteQuery', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: sqlQuery,
                username: localStorage.getItem("username"),
                host: localStorage.getItem("host"),
                password: localStorage.getItem("password")
            })
        }).then(response => response.json()), {
            success: "Query executed successfully!",
            error: "Error executing query",
            pending: "Executing query..."
        }).then(data => {
            if (data.result) {
                setQueryResult(data);
            }
        });
    }

    return (
        <div className={"w-screen mx-10 flex flex-col gap-2"}>
            <Card className="bg-white">
                <CardHeader className="flex items-center justify-center">
                    <DatabaseIcon className="w-6 h-6 mr-2 text-red-500"/>
                    <div>
                        <ToastContainer/>
                        <CardTitle className="text-lg text-center">Query Optimizer</CardTitle>
                        <CardDescription className="text-center">Enter your SQL query below to optimize
                            it.</CardDescription>
                    </div>
                </CardHeader>
                <CardContent className="flex gap-4 pt-4">
                    <div className="grid gap-1.5 w-full">
                        <Label htmlFor="sql">SQL Query</Label>
                        <Textarea id="sql" placeholder="Enter your SQL query here." value={sqlQuery}
                                  onChange={(e) => setSqlQuery(e.target.value)}/>
                    </div>
                    <div className="grid gap-1.5 w-full">
                        <Label htmlFor="optimized">Optimized</Label>
                        <Textarea id="optimized" placeholder="Optimized SQL query" readOnly/>
                    </div>
                </CardContent>
                <CardFooter className="flex gap-4">
                    <Button disabled={!sqlQuery} className="bg-green-500" onClick={validateQuery}>Validate
                        Syntax</Button>
                    <Button disabled={!isValidQuery} className="bg-blue-500" onClick={executeQuery}>Execute
                        Query </Button>
                </CardFooter>
            </Card>
            <Card className="bg-white">
                <CardHeader className="flex items-center justify-center">
                    <CardTitle className="text-lg text-center">Query Result</CardTitle>
                </CardHeader>
                <CardContent>
                    {queryResult?.result && <QueryResultTable result={queryResult.result}/>}
                </CardContent>
            </Card>
        </div>
    )
}

function DatabaseIcon(props: JSX.IntrinsicAttributes & SVGProps<SVGSVGElement>) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <ellipse cx="12" cy="5" rx="9" ry="3"/>
            <path d="M3 5V19A9 3 0 0 0 21 19V5"/>
            <path d="M3 12A9 3 0 0 0 21 12"/>
        </svg>
    )
}
