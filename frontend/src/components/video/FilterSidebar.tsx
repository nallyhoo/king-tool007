import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { DateRange } from "react-day-picker"
import { Calendar } from "@/components/ui/calendar"

export function FilterSidebar() {
    // Dummy state for now
    const date: DateRange | undefined = {
        from: new Date(),
        to: new Date(),
    };

    return (
        <aside className="w-72 border-r bg-background p-6">
            <h2 className="text-xl font-semibold mb-4">Filters</h2>
            <div className="space-y-6">
                {/* Platform checkboxes */}
                <div>
                    <h3 className="font-semibold mb-2">Platform</h3>
                    <div className="space-y-2">
                        <div className="flex items-center space-x-2">
                            <Checkbox id="youtube" />
                            <Label htmlFor="youtube">YouTube</Label>
                        </div>
                        <div className="flex items-center space-x-2">
                            <Checkbox id="vimeo" />
                            <Label htmlFor="vimeo">Vimeo</Label>
                        </div>
                    </div>
                </div>

                {/* Date range picker */}
                <div>
                    <h3 className="font-semibold mb-2">Date Range</h3>
                    <Popover>
                        <PopoverTrigger asChild>
                            <Button variant="outline" className="w-full justify-start text-left font-normal">
                                <span>Pick a date range</span>
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0" align="start">
                            <Calendar
                                mode="range"
                                selected={date}
                                // onSelect={...}
                            />
                        </PopoverContent>
                    </Popover>
                </div>

                {/* More filters go here */}

            </div>
        </aside>
    )
}
