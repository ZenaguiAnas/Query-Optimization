/**
 * v0 by Vercel.
 * @see https://v0.dev/t/lYv1RsyVGmC
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
import { CardTitle, CardDescription, CardHeader, CardContent, CardFooter, Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { JSX, SVGProps } from "react"

export default function HomeComponent
() {
    return (
        <Card className="w-full max-w-lg bg-white">
            <CardHeader className="flex items-center justify-center">
                <DatabaseIcon className="w-6 h-6 mr-2 text-red-500"/>
                <div>
                    <CardTitle className="text-lg text-center">Query Optimizer</CardTitle>
                    <CardDescription className="text-center">Enter your SQL query below to optimize
                        it.</CardDescription>
                </div>
            </CardHeader>
            <CardContent className="flex gap-4 pt-4">
                <div className="grid gap-1.5 w-full">
                    <Label htmlFor="sql">SQL Query</Label>
                    <Textarea id="sql" placeholder="Enter your SQL query here."/>
                </div>
                <div className="grid gap-1.5 w-full">
                    <Label htmlFor="optimized">Optimized</Label>
                    <Textarea id="optimized" placeholder="Optimized SQL query" readOnly/>
                </div>
            </CardContent>
            <CardFooter className="flex">
                <Button className="ml-auto bg-red-500">Optimize</Button>
            </CardFooter>
        </Card>
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
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M3 5V19A9 3 0 0 0 21 19V5" />
      <path d="M3 12A9 3 0 0 0 21 12" />
    </svg>
  )
}
