json.array!(@functions) do |function|
  json.extract! function, :id, :name, :active
  json.url function_url(function, format: :json)
end
