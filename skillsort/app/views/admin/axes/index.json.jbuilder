json.array!(@axes) do |axis|
  json.extract! axis, :id, :name, :description, :value, :active
  json.url axis_url(axis, format: :json)
end
