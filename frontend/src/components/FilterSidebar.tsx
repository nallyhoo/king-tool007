import { Button } from "./ui/button";

export function FilterSidebar() {
  return (
    <aside className="w-80 p-6 bg-gray-50 border-r border-gray-200">
      <h2 className="text-2xl font-bold mb-6">Filters</h2>
      
      {/* Sort Options */}
      <div className="mb-6">
        <h3 className="font-semibold mb-3">Sort By</h3>
        <select className="w-full p-2 border rounded-md">
          <option>Date</option>
          <option>Title</option>
          <option>Duration</option>
          <option>Size</option>
        </select>
      </div>

      {/* Platform Filter */}
      <div className="mb-6">
        <h3 className="font-semibold mb-3">Platform</h3>
        <div className="space-y-2">
          <label className="flex items-center"><input type="checkbox" className="mr-2" /> YouTube</label>
          <label className="flex items-center"><input type="checkbox" className="mr-2" /> Vimeo</label>
        </div>
      </div>

      {/* Quality Filter */}
      <div className="mb-6">
        <h3 className="font-semibold mb-3">Quality</h3>
        <select className="w-full p-2 border rounded-md">
          <option>1080p</option>
          <option>720p</option>
          <option>480p</option>
        </select>
      </div>

      <Button className="w-full">Apply Filters</Button>
    </aside>
  );
}
