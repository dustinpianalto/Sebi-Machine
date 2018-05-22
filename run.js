const Discord = require("discord.js");
const client = new Discord.Client();

const config = require("./src/config/Config.json");
const prefix = config.prefix;

const aliases = require("./src/shared_libs/aliases.json");
const privateConfig = require("./src/config/PrivateConfig.json");

const fs = require("fs");
const commands = fs.readdirSync("./src/cogs").filter(function(e) {
    return e.endsWith(".js");
});


client.on("message", function(message) {
    
    if (message.guild.id != "265828729970753537") {
        return;
    }

    if (message.content.startsWith(config.prefix) == false) {
        return;
    }

    const msg = message.content.replace(prefix, "");

    let command = msg.split(" ")[0];
    const args = msg.split(" ").slice(1);

    command = aliases[command];

    try {

        if (commands.includes(`${command}.js`)) {
            require(`./src/cogs/${command}.js`).run(client, message, args);
        }

    } catch (err) {

        // handling errors

    }

});

client.login(privateConfig["bot-key"]);