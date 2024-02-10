"use client";
import {useState} from 'react';
import {ToastContainer, toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {CardTitle, CardDescription, CardHeader, CardContent, CardFooter, Card} from "@/components/ui/card"
import {Label} from "@/components/ui/label"
import {Textarea} from "@/components/ui/textarea"
import {Button} from "@/components/ui/button"
import {JSX, SVGProps} from "react"
import {QueryResultTable} from "@/components/QueryResultTable";
import {Data} from "@/types";


export default function HomeComponent() {
    const [sqlQuery, setSqlQuery] = useState("");
    // const [optimizedQuery, setOptimizedQuery] = useState("");
    // const [validationResult, setValidationResult] = useState("");
    const [queryResult, setQueryResult] = useState<Data | null>(null);

    // todo: replace with the actual backend URL
    const backendUrl = "http://localhost:5000";

    const validateQuery = async () => {
        try {
            const response = await fetch(backendUrl + '/ValidateSQL', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({query: sqlQuery})
            });

            const data = await response.json();
            // setValidationResult(data);
            console.log(data);

            if (data.result == "Valid SQL Query") {
                console.log(data.result);
                // Afficher le message "Valid SQL Query" en cas de succès
                toast.success("Valid SQL Query");
            } else {
                // Afficher le message d'erreur retourné par le backend en cas d'erreur
                toast.error(data.error);
            }
        } catch (error) {

        }
    };


    async function executeQuery() {
        try {
            const response = await fetch(backendUrl + '/ExecuteQuery', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({query: sqlQuery})
            });

            const data = await response.json();

            if (data.result) {
                setQueryResult(data);
                // Afficher le message "Valid SQL Query" en cas de succès
                toast.success("Query executed successfully!");
            } else {
                // Afficher le message d'erreur retourné par le backend en cas d'erreur
                toast.error("Error executing query");
            }
        } catch (error) {

        }
    }


    return (<div className={"w-screen mx-10 flex flex-col gap-2"}>
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
                    <Button disabled={!sqlQuery} className="bg-blue-500" onClick={executeQuery}>Execute
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
