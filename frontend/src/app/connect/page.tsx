import { DbConnection } from "@/components/DbConnection";


export default function Connect() {
    return (
        <div className={"flex justify-center mt-10"}>
            <DbConnection></DbConnection>
        </div>
    );
}
