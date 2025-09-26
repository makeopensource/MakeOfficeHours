import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from "../ui/form";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";

interface QueueFormProps {
  role: "student" | "ta";
  onSubmit: (data: any) => void;  // Callback to handle form submission
  onClose: () => void;
}

const studentFormSchema = z.object({
  ubit: z.string().min(1, "Enter a valid UBIT Name").max(10),
  name: z.string().min(1, "Enter a valid name").max(20),
  issue: z.string().min(1, "Enter a valid reason").max(100),
});

const taFormSchema = z.object({
  ubit: z.string().min(1, "Enter a valid UBIT Name").max(10),
  name: z.string().min(1, "Enter a valid name").max(20),
  issue: z.string().min(1, "Enter a valid reason").max(100),
});

const schema = z.union([studentFormSchema, taFormSchema]);

export const QueueForm: React.FC<QueueFormProps> = ({ role, onSubmit, onClose }) => {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: {
      ubit: "",
      name: "",
      issue: "",
    },
  });

  const handleFormSubmit = (values: z.infer<typeof schema>) => {
    onSubmit(values);  // Send data to parent component
    onClose();
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleFormSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="ubit"
          render={({ field }) => (
            <FormItem>
              <FormLabel>UBIT</FormLabel>
              <FormControl>
                <Input type="text" placeholder="Enter Student's UBIT" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input type="text" placeholder="Enter Student's Name" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Assignment Type */}
        {/* <FormField
          control={form.control}
          name="assignment"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Assignment</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger className="bg-transparent text-muted-foreground">
                    <SelectValue placeholder="Select the assignment" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent className=" text-muted-foreground">
                  <SelectItem value="Task1">Task 1</SelectItem>
                  <SelectItem value="Task2">Task 2</SelectItem>
                  <SelectItem value="Task3">Task 3</SelectItem>
                  <SelectItem value="Task4">Task 4</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        /> */}

        <FormField
          control={form.control}
          name="issue"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Issue</FormLabel>
              <FormControl>
                <Input type="text" placeholder="Describe the issue" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        
        <div className="flex justify-center py-4 px-5 gap-3">
          <Button type="button" variant={"primary"} size={"default"} className="w-1/2 font-semibold" onClick={onClose}>Cancel</Button>
          <Button type="submit" variant={"default"} size={"default"} className="w-1/2 font-semibold">Join Queue</Button>
        </div>

      </form>
    </Form>
  );
};
