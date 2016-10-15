class CreateAxes < ActiveRecord::Migration
  def change
    create_table :axes do |t|
      t.string :name
      t.text :description
      t.integer :value
      t.boolean :active

      t.timestamps
    end
  end
end
