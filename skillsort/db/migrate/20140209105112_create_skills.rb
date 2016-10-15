class CreateSkills < ActiveRecord::Migration
  def change
    create_table :skills do |t|
      t.string :name
      t.text :description
      t.boolean :active

      t.timestamps
    end
  end
end
