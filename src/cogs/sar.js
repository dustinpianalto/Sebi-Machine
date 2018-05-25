const Discord = require("discord.js");

exports.run = async function(client, message, args) {

    /*
        aliases: sar, selfrole, selfroles

        examples: 
        - S!selfrole get 1 (adds heroku helper role)
        - S!sar remove 3 (removes rewrite helper role)
        - S!sar list (shows all roles)
    */

    function roleFinder(query) {
        return message.guild.roles.find(function(r) {
            return r.name.includes(query)
        }).id;
    }

    const type = args[0]; // can be get, remove or list

    if (type == "list") {

        const embed = new Discord.RichEmbed()
            .setTitle("List of Self Assigned Roles")
            .setDescription("Usage: `S!sar [ get | remove | list ] [ number ]`")
            .addField("1. Heroku Helper", "S!sar get 1", true)
            .addField("2. JS Helper", "S!sar get 2", true)
            .addField("3. Rewrite Helper", "S!sar get 3", true)
            .setColor("AQUA");

        return message.channel.send({
            embed: embed
        });

    }

    const roles = [roleFinder("Heroku"), roleFinder("JS"), roleFinder("Rewrite")];

    let choice = args[1]; // can be 1, 2 or 3

    // if the choice is not 1, 2 or 3
    if (/^[123]$/.test(choice) == false) {
        return message.channel.send("Enter a valid role number!"); // returns error message
    } else {
        choice -= 1; // because array indexing starts from 0. when they choose 1 it should be roles[0]
    }

    switch (type) {

        case "get":
            message.member.addRole(roles[choice]);
            message.channel.send("Added the role you specified!"); // confirmation message
            break;

        case "remove":
            message.member.removeRole(roles[choice]);
            message.channel.send("Removed the role you specified!"); // confirmation message
            break;

        default:
            return; // when it is neither get nor remove
            break;

    }

}